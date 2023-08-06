import collections
from types import ModuleType
import typing as tp

import numpy as np
import sympy as sym

from cocos import numerics as cn
from cocos.numerics.data_types import NumericArray
from cocos.utilities import check_and_make_sequence
from cocos.numerics.numerical_package_selector import \
    select_num_pack, \
    get_gpu_and_num_pack_by_dtype_from_iterable
from cocos.symbolic.translations import COCOS_TRANSLATIONS


################################################################################
# Works for both Matrices and Arrays
################################################################################
def _compute_replacement_functions(
        replacement_functions_cpu: tp.Tuple[tp.Callable, ...],
        replacement_functions_gpu: tp.Tuple[tp.Callable, ...],
        perform_cse: bool,
        state_vectors: tp.Tuple,
        t: float,
        gpu: bool,
        number_of_state_variables: int) \
        -> tp.Tuple[tp.Tuple, int]:

    R = max([state_argument.size
             for state_argument
             in state_vectors
             if isinstance(state_argument, (np.ndarray, cn.ndarray))] + [1])

    if number_of_state_variables != len(state_vectors):
        raise ValueError(f"The number of state vectors({len(state_vectors)}) "
                         f"does not match the number of variables in the "
                         f"function({number_of_state_variables}).")

    arguments = [t] + state_vectors
    if perform_cse:
        for k in range(len(replacement_functions_cpu)):
            if gpu:
                arguments.append(replacement_functions_gpu[k](*arguments))
            else:
                arguments.append(replacement_functions_cpu[k](*arguments))

    return arguments, R


################################################################################
# General Arrays
################################################################################
def lambdify_array_with_modules(
        symbols: tp.Tuple[sym.Symbol, ...],
        array_expression: tp.Union[sym.Array, sym.MatrixBase],
        numeric_time_functions: tp.Dict[str, tp.Callable],
        modules: tp.Tuple[str, ...]) \
        -> tp.Tuple[tp.Callable, ...]:

    if not isinstance(modules, list):
        modules = list(modules)

    if not (isinstance(array_expression, sym.Array) or
            isinstance(array_expression, sym.MatrixBase)):
        raise TypeError(f"symbolic_matrix_expression must be an instance of "
                        f"sympy.ArrayBase or sympy.MatrixBase "
                        f"but is of type {type(array_expression)}")

    n = (np.prod(array_expression.shape)).item()
    result = []
    for i in range(n):
        index = tuple(np.unravel_index(i, array_expression.shape, order='F'))
        result.append(sym.lambdify(symbols,
                                   array_expression[index],
                                   modules=[numeric_time_functions] + modules))

    return tuple(result)


def lambdify_array(
        symbols: tp.Tuple[sym.Symbol, ...],
        array_expression: tp.Union[sym.Array, sym.MatrixBase],
        numeric_time_functions: tp.Optional[tp.Dict[str, tp.Callable]] = None) \
        -> tp.Tuple[tp.Tuple[tp.Callable, ...], tp.Tuple[tp.Callable, ...]]:

    if numeric_time_functions is None:
        numeric_time_functions = dict()

    functions_cpu = lambdify_array_with_modules(symbols,
                                                array_expression,
                                                numeric_time_functions,
                                                ('numpy', ))

    functions_gpu = lambdify_array_with_modules(symbols,
                                                array_expression,
                                                numeric_time_functions,
                                                (COCOS_TRANSLATIONS, ))

    return functions_cpu, functions_gpu


def _compute_result_internal(R: int,
                             dimensions: tp.Tuple[int, ...],
                             arguments,
                             functions_cpu: tp.Tuple[tp.Callable, ...],
                             functions_gpu: tp.Tuple[tp.Callable, ...],
                             pre_attach: bool,
                             gpu: bool,
                             dtype: np.generic) \
        -> NumericArray:

    num_pack = select_num_pack(gpu)
    if gpu:
        functions = functions_gpu
    else:
        functions = functions_cpu

    n = (np.prod(dimensions)).item()

    if pre_attach:
        dimension_index = tuple([R] + list(dimensions))
    else:
        dimension_index = tuple(list(dimensions) + [R])

    result = num_pack.zeros(dimension_index, dtype=dtype)

    for i in range(n):
        index = tuple(np.unravel_index(i, dimensions, order='F'))

        function = functions[i]

        if pre_attach:
            location_index = tuple([slice(None)] + list(index))
        else:
            location_index = tuple(list(index) + [slice(None)])

        evaluated_function = function(*arguments)
        result[location_index] = evaluated_function

    return result


################################################################################
# Sequences of Lambdified Array, Matrix, and Vector-Expressions
################################################################################
class LambdifiedArrayExpressions(object):
    def __init__(
        self,
        argument_symbols: tp.Tuple[sym.Symbol],
        time_symbol: sym.Symbol,
        symbolic_array_expressions: tp.Tuple[tp.Union[sym.Array,
                                                      sym.Matrix],
                                             ...],
        numeric_time_functions: tp.Optional[tp.Dict[str, tp.Callable]] = None,
        squeeze_column_vectors: tp.Optional[tp.Tuple[bool, ...]] = None,
        perform_cse: bool = True,
        lazy_initialization: bool = False,
        pre_attach: tp.Optional[tp.Tuple[bool, ...]] = None,
        dtype: np.generic = np.float32):

        if numeric_time_functions is None:
            numeric_time_functions = dict()

        symbolic_array_expressions \
            = tuple(check_and_make_sequence(symbolic_array_expressions,
                                            sym.Matrix))

        if pre_attach is None:
            pre_attach = len(symbolic_array_expressions) * [True]
        pre_attach = check_and_make_sequence(pre_attach, bool)

        if squeeze_column_vectors is None:
            squeeze_column_vectors = len(symbolic_array_expressions) * [False]
        squeeze_column_vectors = check_and_make_sequence(squeeze_column_vectors,
                                                         bool)

        if not (len(symbolic_array_expressions) == len(pre_attach) and
                len(symbolic_array_expressions) == len(squeeze_column_vectors)):
            raise ValueError("symbolic_matrix_expressions, pre_attach, and "
                             "squeeze_column_vectors must have the same number "
                             "of elements")

        self._argument_symbols = argument_symbols
        self._time_symbol = time_symbol
        self._symbolic_array_expressions = symbolic_array_expressions
        self._numeric_time_functions = numeric_time_functions
        self._squeeze_column_vectors = squeeze_column_vectors
        self._symbols = tuple([time_symbol] + list(argument_symbols))

        self._perform_cse = perform_cse
        self._pre_attach = pre_attach
        self._dtype = dtype

        self._shapes \
            = tuple([symbolic_array_expression.shape
                     for symbolic_array_expression
                     in symbolic_array_expressions])

        if lazy_initialization:
            self._functions_cpu = None
            self._functions_gpu = None
        else:
            self._perform_initialization()

    def _perform_initialization(self):
        self._functions_cpu = []
        self._functions_gpu = []
        if self._perform_cse:
            repl, redu = sym.cse(self._symbolic_array_expressions,
                                 optimizations='basic')

            replacement_functions_cpu = []
            replacement_functions_gpu = []
            syms = [self._time_symbol] + list(self._argument_symbols)
            for i, v in enumerate(repl):
                replacement_functions_cpu.append(
                    sym.lambdify(syms,
                                 v[1],
                                 modules=[self._numeric_time_functions,
                                          'numpy']))

                replacement_functions_gpu.append(
                    sym.lambdify(
                        syms,
                        v[1],
                        modules=[self._numeric_time_functions,
                                 COCOS_TRANSLATIONS]))

                syms.append(v[0])

            self._replacement_functions_cpu = tuple(replacement_functions_cpu)
            self._replacement_functions_gpu = tuple(replacement_functions_gpu)

            for symbolic_matrix_expression in redu:
                functions_cpu, functions_gpu \
                    = lambdify_array(tuple(syms),
                                     symbolic_matrix_expression,
                                     self._numeric_time_functions)

                self._functions_cpu.append(functions_cpu)
                self._functions_gpu.append(functions_gpu)
        else:
            for symbolic_matrix_expression in self._symbolic_array_expressions:
                functions_cpu, functions_gpu \
                    = lambdify_array(self._symbols,
                                     symbolic_matrix_expression,
                                     self._numeric_time_functions)

                self._functions_cpu.append(functions_cpu)
                self._functions_gpu.append(functions_gpu)

    @property
    def shapes(self) -> tp.Tuple[tp.Tuple[int, ...], ...]:
        return self._shapes

    def is_column_vector(self, i: int) -> bool:
        shape = self._symbolic_array_expressions[i].shape
        return len(shape) == 1 \
               or all([dim == 1
                       for dim
                       in shape[1:]])

    def is_row_vector(self, i: int) -> bool:
        shape = self._symbolic_array_expressions[i].shape
        if len(shape < 2):
            return False
        else:
            return shape[0] == 1 and \
                   (len(shape) == 2 or
                    all([dim == 1
                         for dim
                         in shape[2:]]))

    @property
    def argument_symbols(self) -> tp.Tuple[sym.Symbol, ...]:
        return self._argument_symbols

    @property
    def number_of_state_variables(self) -> int:
        return len(self._argument_symbols)

    @property
    def time_symbol(self) -> sym.Symbol:
        return self._time_symbol

    @property
    def symbolic_array_expressions(self) -> tp.Tuple[sym.Matrix, ...]:
        return self._symbolic_array_expressions

    @property
    def numeric_time_functions(self) -> tp.Dict[str, tp.Callable]:
        return self._numeric_time_functions

    @property
    def symbols(self) -> tp.Tuple[sym.Symbol, ...]:
        return self._symbols

    @property
    def number_of_variables(self) -> int:
        return len(self._symbols)

    @property
    def dtype(self) -> np.generic:
        return self._dtype

    def evaluate_with_list_of_state_vectors(
            self,
            list_of_state_vectors: tp.Tuple[NumericArray, ...],
            t: float,
            gpu: bool = False) \
            -> tp.Tuple[NumericArray, ...]:

        if self._functions_cpu is None or self._functions_gpu is None:
            self._perform_initialization()

        arguments, R \
            = _compute_replacement_functions(self._replacement_functions_cpu,
                                             self._replacement_functions_gpu,
                                             self._perform_cse,
                                             list_of_state_vectors,
                                             t,
                                             gpu,
                                             self.number_of_state_variables)

        results = []
        for i, (shape,
                pre_attach,
                functions_cpu,
                functions_gpu,
                squeeze_column_vector) in \
                enumerate(zip(self.shapes,
                              self._pre_attach,
                              self._functions_cpu,
                              self._functions_gpu,
                              self._squeeze_column_vectors)):
            is_column_vector = self.is_column_vector(i)

            if is_column_vector and squeeze_column_vector:
                dimensions = (shape[0], )
            else:
                dimensions = shape

            result = _compute_result_internal(R,
                                              dimensions,
                                              arguments,
                                              functions_cpu,
                                              functions_gpu,
                                              pre_attach,
                                              gpu,
                                              self.dtype)
            results.append(result)

        return tuple(results)

    def evaluate(self,
                 state_matrices: tp.Tuple[NumericArray, ...],
                 t: float) \
            -> tp.Tuple[NumericArray, ...]:

        if not isinstance(state_matrices, collections.Sequence):
            if isinstance(state_matrices, (np.ndarray, cn.ndarray)):
                state_matrices = [state_matrices]
            else:
                raise TypeError("state_variables must be of type "
                                "Sequence[Union[numpy.ndarray, cocos.ndarray]]")

        gpu, num_pack \
            = get_gpu_and_num_pack_by_dtype_from_iterable(state_matrices)
        list_of_state_vectors = []
        for state_matrix in state_matrices:
            if state_matrix.ndim > 1:
                for i in range(state_matrix.shape[1]):
                    list_of_state_vectors.append((state_matrix[:, i]))
            else:
                list_of_state_vectors.append(state_matrix)

        return self.evaluate_with_list_of_state_vectors(list_of_state_vectors, t, gpu)


class LambdifiedMatrixExpressions(LambdifiedArrayExpressions):
    def __init__(
         self,
         argument_symbols: tp.Tuple[sym.Symbol, ...],
         time_symbol: sym.Symbol,
         symbolic_matrix_expressions: tp.Tuple[sym.Matrix, ...],
         numeric_time_functions: tp.Optional[tp.Dict[str, tp.Callable]] = None,
         squeeze_column_vectors: tp.Optional[tp.Tuple[bool, ...]] = None,
         perform_cse: bool = True,
         lazy_initialization: bool = False,
         pre_attach: tp.Optional[tp.Tuple[bool, ...]] = None,
         dtype: np.generic = np.float32):

        if numeric_time_functions is None:
            numeric_time_functions = dict()

        super().__init__(argument_symbols,
                         time_symbol,
                         symbolic_matrix_expressions,
                         numeric_time_functions,
                         squeeze_column_vectors,
                         perform_cse,
                         lazy_initialization,
                         pre_attach,
                         dtype)

        rows = []
        cols = []

        for symbolic_matrix_expression in symbolic_matrix_expressions:
            r, c = symbolic_matrix_expression.shape
            rows.append(r)
            cols.append(c)

        self._rows = tuple(rows)
        self._cols = tuple(cols)

    @property
    def rows(self) -> tp.Tuple[int, ...]:
        return self._rows

    @property
    def cols(self) -> tp.Tuple[int, ...]:
        return self._cols

    @property
    def symbolic_matrix_expressions(self) -> tp.Tuple[sym.Matrix, ...]:
        return self.symbolic_array_expressions


################################################################################
# Single Lambdified Array, Matrix, and Vector-Expressions
################################################################################
class LambdifiedArrayExpression(object):
    def __init__(
         self,
         argument_symbols: tp.Tuple[sym.Symbol, ...],
         time_symbol: sym.Symbol,
         symbolic_array_expression: tp.Union[sym.Matrix, sym.Array],
         numeric_time_functions: tp.Optional[tp.Dict[str, tp.Callable]] = None,
         squeeze_column_vector: bool = False,
         perform_cse: bool = True,
         lazy_initialization: bool = False,
         pre_attach: bool = True,
         dtype: np.generic = np.float32):

        self._lambdified_array_expressions = \
            LambdifiedArrayExpressions(
                argument_symbols=argument_symbols,
                time_symbol=time_symbol,
                symbolic_array_expressions=(symbolic_array_expression, ),
                numeric_time_functions=numeric_time_functions,
                squeeze_column_vectors=(squeeze_column_vector, ),
                perform_cse=perform_cse,
                lazy_initialization=lazy_initialization,
                pre_attach=(pre_attach, ),
                dtype=dtype)

    @property
    def is_column_vector(self) -> bool:
        return self._lambdified_array_expressions.is_column_vector(0)

    @property
    def is_row_vector(self) -> bool:
        return self._lambdified_array_expressions.is_row_vector(0)

    @property
    def argument_symbols(self) -> tp.Tuple[sym.Symbol, ...]:
        return self._lambdified_array_expressions.argument_symbols

    @property
    def number_of_state_variables(self) -> int:
        return self._lambdified_array_expressions.number_of_state_variables

    @property
    def time_symbol(self) -> sym.Symbol:
        return self._lambdified_array_expressions.time_symbol

    @property
    def symbolic_array_expression(self) -> sym.Matrix:
        return self._lambdified_array_expressions.symbolic_array_expressions[0]

    @property
    def numeric_time_functions(self) -> tp.Dict[str, tp.Callable]:
        return self._lambdified_array_expressions.numeric_time_functions

    @property
    def symbols(self) -> tp.Tuple[sym.Symbol, ...]:
        return self._lambdified_array_expressions.symbols

    @property
    def number_of_variables(self) -> int:
        return self._lambdified_array_expressions.number_of_variables

    def evaluate_with_list_of_state_vectors(
            self,
            list_of_state_vectors: tp.Tuple[NumericArray, ...],
            t: float,
            gpu: bool = False) \
            -> NumericArray:

        return (self
                ._lambdified_array_expressions
                .evaluate_with_list_of_state_vectors(list_of_state_vectors,
                                                     t,
                                                     gpu)[0])

    def evaluate(self,
                 state_matrices: tp.Tuple[NumericArray, ...],
                 t: float) -> NumericArray:
        return self._lambdified_array_expressions.evaluate(state_matrices, t)[0]


class LambdifiedMatrixExpression(LambdifiedArrayExpression):
    def __init__(
         self,
         argument_symbols: tp.Tuple[sym.Symbol, ...],
         time_symbol: sym.Symbol,
         symbolic_matrix_expression: sym.Matrix,
         numeric_time_functions: tp.Optional[tp.Dict[str, tp.Callable]] = None,
         squeeze_column_vector: bool = False,
         perform_cse: bool = True,
         lazy_initialization: bool = False,
         pre_attach: bool = True,
         dtype: np.generic = np.float32):

        super().__init__(argument_symbols,
                         time_symbol,
                         symbolic_matrix_expression,
                         numeric_time_functions,
                         squeeze_column_vector,
                         perform_cse,
                         lazy_initialization,
                         pre_attach,
                         dtype)

    @property
    def rows(self) -> int:
        return (self
                ._lambdified_array_expressions
                .symbolic_array_expressions[0]
                .shape[0])

    @property
    def cols(self) -> int:
        return (self
                ._lambdified_array_expressions
                .symbolic_array_expressions[0].shape[1])


class LambdifiedVectorExpression(LambdifiedMatrixExpression):
    def __init__(
         self,
         argument_symbols: tp.Tuple[sym.Symbol, ...],
         time_symbol: sym.Symbol,
         symbolic_vector_expression: sym.Matrix,
         numeric_time_functions: tp.Optional[tp.Dict[str, tp.Callable]] = None,
         perform_cse: bool = True,
         lazy_initialization: bool = False,
         pre_attach: bool = True,
         dtype: np.generic = np.float32):

        super().__init__(argument_symbols,
                         time_symbol,
                         symbolic_vector_expression,
                         numeric_time_functions,
                         True,
                         perform_cse,
                         lazy_initialization,
                         pre_attach,
                         dtype)


def lambdify(args,
             expr,
             modules: tp.Optional[tp.Tuple] = None,
             printer: tp.Optional[tp.Tuple] = None,
             use_imps: bool = True,
             dummify: bool = True):
    if modules is None:
        modules = []

    return sym.lambdify(args,
                        expr,
                        modules=list(modules) + [COCOS_TRANSLATIONS],
                        printer=printer,
                        use_imps=use_imps,
                        dummify=dummify)
