from numpy import size as numpy_size

from . import PropertiesData

from ..functions    import parse_indices
from ..functions    import equivalent as cf_equivalent
from ..functions    import inspect    as cf_inspect
from ..functions    import (_DEPRECATION_ERROR_KWARGS,
                            _DEPRECATION_ERROR_METHOD,
                            _DEPRECATION_ERROR_ATTRIBUTE)
from ..query        import Query
from ..units        import Units

from ..data.data import Data

_debug=False

_units_None = Units()

_month_units = ('month', 'months')
_year_units  = ('year', 'years', 'yr')


class PropertiesDataBounds(PropertiesData):
    '''Mixin class for a data array with descriptive properties and cell
    bounds.

    '''
    def __getitem__(self, indices):
        '''Return a subspace of the field construct defined by indices.

    x.__getitem__(indices) <==> x[indices]

        '''
        if indices is Ellipsis:
            return self.copy()

        # Parse the index
        if not isinstance(indices, tuple):
            indices = (indices,)

        arg0 = indices[0]
        if isinstance(arg0, str) and arg0 == 'mask':
            auxiliary_mask = indices[:2]
            indices2       = indices[2:]
        else:
            auxiliary_mask = None
            indices2       = indices
          
        indices, roll = parse_indices(self.shape, indices2, cyclic=True)

        if roll:
            new = self
            data = self.data
            axes = data._axes
            cyclic_axes = data._cyclic
            for iaxis, shift in roll.items():
                if axes[iaxis] not in cyclic_axes:
                    raise IndexError(
                        "Can't do a cyclic slice on a non-cyclic axis")

                new = new.roll(iaxis, shift)
        else:
            new = self.copy() #data=False)

        data = self.data

        if auxiliary_mask:
            findices = tuple(auxiliary_mask) + tuple(indices)
        else:
            findices = tuple(indices)

        if _debug:
            cname = self.__class__.__name__
            print('{}.__getitem__: shape    = {}'.format(cname, self.shape)) # Pragma: no cover
            print('{}.__getitem__: indices2 = {}'.format(cname, indices2)) # Pragma: no cover
            print('{}.__getitem__: indices  = {}'.format(cname, indices)) # Pragma: no cover
            print('{}.__getitem__: findices = {}'.format(cname, findices)) # Pragma: no cover

        new.set_data(data[findices], copy=False)

        # Subspace the bounds, if there are any
        bounds = self.get_bounds(None)
        if bounds is not None:                
            bounds_data = bounds.get_data(None)
            if bounds_data is not None:
                findices = list(findices)
                if data.ndim <= 1:
                    index = indices[0]
                    if isinstance(index, slice):
                        if index.step < 0:
                            # This scalar or 1-d variable has been
                            # reversed so reverse its bounds (as per
                            # 7.1 of the conventions)
                            findices.append(slice(None, None, -1))
                    elif data.size > 1 and index[-1] < index[0]:
                        # This 1-d variable has been reversed so
                        # reverse its bounds (as per 7.1 of the
                        # conventions)
                        findices.append(slice(None, None, -1))                    
                #--- End: if

                if auxiliary_mask:
                    findices[1] = [mask.insert_dimension(-1) for mask in findices[1]]

                if _debug:
                    print('{}.__getitem__: findices for bounds ='.format(
                        self.__class__.__name__, findices)) # pragma: no cover

                new.bounds.set_data(bounds_data[tuple(findices)], copy=False)
        #--- End: if

        # Remove the direction, as it may now be wrong
        new._custom.pop('direction', None)

        # Return the new bounded variable
        return new


    def __eq__(self, y):
        '''The rich comparison operator ``==``

    x.__eq__(y) <==> x==y

        '''
        return self._binary_operation(y, '__eq__', False)


    def __ne__(self, y):
        '''The rich comparison operator ``!=``

    x.__ne__(y) <==> x!=y

        '''
        return self._binary_operation(y, '__ne__', False)

    
    def __ge__(self, y):
        '''The rich comparison operator ``>=``

    x.__ge__(y) <==> x>=y

        '''
        return self._binary_operation(y, '__ge__', False)


    def __gt__(self, y):
        '''The rich comparison operator ``>``

    x.__gt__(y) <==> x>y

        '''
        return self._binary_operation(y, '__gt__', False)


    def __le__(self, y):
        '''The rich comparison operator ``<=``

    x.__le__(y) <==> x<=y

        '''
        return self._binary_operation(y, '__le__', False)


    def __lt__(self, y):
        '''The rich comparison operator ``<``

    x.__lt__(y) <==> x<y

        '''
        return self._binary_operation(y, '__lt__', False)

    
    def __and__(self, other):
        '''The binary bitwise operation ``&``

    x.__and__(y) <==> x&y

        '''
        return self._binary_operation(other, '__and__', False)


    def __iand__(self, other):
        '''The augmented bitwise assignment ``&=``

    x.__iand__(y) <==> x&=y

        '''
        return self._binary_operation(other, '__iand__', False)


    def __rand__(self, other):
        '''The binary bitwise operation ``&`` with reflected operands

    x.__rand__(y) <==> y&x

        '''
        return self._binary_operation(other, '__rand__', False)


    def __or__(self, other):
        '''The binary bitwise operation ``|``

    x.__or__(y) <==> x|y

        '''
        return self._binary_operation(other, '__or__', False)


    def __ior__(self, other):
        '''The augmented bitwise assignment ``|=``

    x.__ior__(y) <==> x|=y

        '''
        return self._binary_operation(other, '__ior__', False)


    def __ror__(self, other):
        '''The binary bitwise operation ``|`` with reflected operands

    x.__ror__(y) <==> y|x

        '''
        return self._binary_operation(other, '__ror__', False)

    def __xor__(self, other):
        '''The binary bitwise operation ``^``

    x.__xor__(y) <==> x^y

        '''
        return self._binary_operation(other, '__xor__', False)


    def __ixor__(self, other):
        '''The augmented bitwise assignment ``^=``

    x.__ixor__(y) <==> x^=y

        '''
        return self._binary_operation(other, '__ixor__', False)


    def __rxor__(self, other):
        '''The binary bitwise operation ``^`` with reflected operands

    x.__rxor__(y) <==> y^x

        '''
        return self._binary_operation(other, '__rxor__', False)


    def __lshift__(self, y):
        '''The binary bitwise operation ``<<``

    x.__lshift__(y) <==> x<<y

        '''
        return self._binary_operation(y, '__lshift__', False)


    def __ilshift__(self, y):
        '''The augmented bitwise assignment ``<<=``

    x.__ilshift__(y) <==> x<<=y

        '''
        return self._binary_operation(y, '__ilshift__', False)


    def __rlshift__(self, y):
        '''The binary bitwise operation ``<<`` with reflected operands

    x.__rlshift__(y) <==> y<<x

        '''
        return self._binary_operation(y, '__rlshift__', False)


    def __rshift__(self, y):
        '''The binary bitwise operation ``>>``

    x.__lshift__(y) <==> x>>y

        '''
        return self._binary_operation(y, '__rshift__', False)

    
    def __irshift__(self, y):
        '''The augmented bitwise assignment ``>>=``

    x.__irshift__(y) <==> x>>=y

        '''
        return self._binary_operation(y, '__irshift__', False)


    def __rrshift__(self, y):
        '''The binary bitwise operation ``>>`` with reflected operands

    x.__rrshift__(y) <==> y>>x

        '''
        return self._binary_operation(y, '__rrshift__', False)


    # ----------------------------------------------------------------
    # Private methods
    # ----------------------------------------------------------------
    def _binary_operation(self, other, method, bounds=True):
        '''Implement binary arithmetic and comparison operations.

    The operations act on the construct's data array with the numpy
    broadcasting rules.
    
    If the construct has bounds then they are operated on with the
    same data as the construct's data.
    
    It is intended to be called by the binary arithmetic and comparison
    methods, such as `!__sub__` and `!__lt__`.
    
    :Parameters:
    
        other:
    
        method: `str`
            The binary arithmetic or comparison method name (such as
            ``'__imul__'`` or ``'__ge__'``).
    
        bounds: `bool`, optional
            If False then ignore the bounds and remove them from the
            result. By default the bounds are operated on as well.
    
    :Returns:
    
            A new construct, or the same construct if the operation
            was in-place.

        '''
        inplace = method[2] == 'i'

        has_bounds = bounds and self.has_bounds()
        
        if has_bounds and inplace and other is self:
            other = other.copy()
        
        new = super()._binary_operation(other, method)

        if has_bounds:
#            try:
#                other_has_bounds = other.has_bounds()
#            except AttributeError:
#                other_has_bounds = False

#            if other_has_bounds:
#                new_bounds = self.bounds._binary_operation(other.bounds, method)
#            else:                
            if numpy_size(other) > 1:
                try:
                    other = other.insert_dimension(-1)
                except AttributeError:
                    other = numpy_expand_dims(other, -1)
            #-- End: if
                
            new_bounds = self.bounds._binary_operation(other, method)

            if not inplace:
                new.set_bounds(new_bounds, copy=False)
        #--- End: if

        if not bounds and new.has_bounds():
            new.del_bounds()
            
        if inplace:
            return self
        else:
            return new


    def _equivalent_data(self, other, rtol=None, atol=None,
                         verbose=False):
        '''TODO

    Two real numbers ``x`` and ``y`` are considered equal if
    ``|x-y|<=atol+rtol|y|``, where ``atol`` (the tolerance on absolute
    differences) and ``rtol`` (the tolerance on relative differences) are
    positive, typically very small numbers. See the *atol* and *rtol*
    parameters.
    
    :Parameters:
    
        atol: `float`, optional
            The tolerance on absolute differences between real
            numbers. The default value is set by the `ATOL` function.
    
        rtol: `float`, optional
            The tolerance on relative differences between real
            numbers. The default value is set by the `RTOL` function.
    
    :Returns:
    
        `bool`
    
        '''
        self_bounds = self.get_bounds(None)
        other_bounds = other.get_bounds(None)
        hasbounds = self_bounds is not None
        
        if hasbounds != (other_bounds is not None):
            # add traceback
            if verbose:
                print('one has bounds, the other not TODO') # pragma: no cover
            return False

        try:
            direction0 = self.direction()
            direction1 = other.direction()
            if (direction0 != direction1 and 
                direction0 is not None and direction1 is not None):
                other = other.flip()
        except AttributeError:
            pass
        
        # Compare the data arrays
        if not super()._equivalent_data(
                other, rtol=rtol, atol=atol, verbose=verbose):
            if verbose:
                print('non equivaelnt data arrays TODO') # pragma: no cover
            return False

        if hasbounds:
            # Compare the bounds
            if not self_bounds._equivalent_data(other_bounds,
                                                rtol=rtol, atol=atol,
                                                verbose=verbose):
                if verbose:
                    print('{}: Non-equivalent bounds data: {!r}, {!r}'.format(
                        self.__class__.__name__, self_bounds.data, other_bounds.data)) # pragma: no cover
                return False
        #--- End: if

        # Still here? Then the data are equivalent.
        return True


    def _YMDhms(self, attr):
        '''TODO
        '''
        out = super()._YMDhms(attr)
        out.del_bounds(None)
        return out

    
    def _matching_values(self, value0, value1, units=False):
        '''TODO

        '''
        if value1 is None:            
            return False

        if units and isinstance(value0, str):
            return Units(value0).equals(Units(value1))
        
        if isinstance(value0, Query):
            return bool(value0.evaluate(value1)) # TODO vectors
        else:
            try:
                return value0.search(value1)
            except (AttributeError, TypeError):
                return self._equals(value1, value0)
        #--- End: if

        return False

    
    def _apply_data_operation(
            self, oper_name, *oper_args, bounds=True, inplace=False,
            i=False, **oper_kwargs):
        '''Define an operation that can be applied to the data array.

        * 'oper_name' should be the string name for the desired operation
          as it is defined (its method name) under the Data class, e.g.
          'sin' to apply 'Data.sin'
        * any positional or keyword arguments required in the operation
          call should be passed through via *oper_args and **oper_kwargs.
        '''
        if i:
            _DEPRECATION_ERROR_KWARGS(self, oper_name, i=True) # pragma: no cover
 
        v = getattr(super(), oper_name)(*oper_args, inplace=inplace,
                                        **oper_kwargs)
        if inplace:
            v = self

        if bounds:
            bounds = v.get_bounds(None)
            if bounds is not None:
                getattr(bounds, oper_name)(*oper_args, inplace=True,
                                           **oper_kwargs)
        #--- End: if

        if inplace:
            v = None
        return v


    # ----------------------------------------------------------------
    # Attributes
    # ----------------------------------------------------------------
    @property
    def cellsize(self):
        '''The cell sizes.

    If there are no cell bounds then the cell sizes are all zero.

    .. versionadded:: 2.0

    **Examples:**
    
    >>> print(c.bounds.array)
    [[-90. -87.]
     [-87. -80.]
     [-80. -67.]]
    >>> c.cellsize
    <CF Data(3,): [3.0, 7.0, 13.0] degrees_north>
    >>> print(d.cellsize.array)
    [  3.   7.  13.]
    >>> b = c.del_bounds()
    >>> c.cellsize
    <CF Data(3,): [0, 0, 0] degrees_north>

        '''
        data = self.get_bounds_data(None)
        if data is not None:
            if data.shape[-1] != 2:
                raise ValueError(
                    "Can only calculate cell sizes from bounds when there are exactly two bounds per cell. Got {}".format(
                        data.shape[-1]))
            
            out = abs(data[..., 1] - data[..., 0])
            out.squeeze(-1, inplace=True)                
            return out
        else:
            data = self.get_data(None)
            if data is not None:
                return Data.zeros(self.shape, units=self.Units)
        #--- End: if

        raise AttributeError(
            "Can't get cell sizes when there are no bounds nor coordinate data")

    
    @property
    def dtype(self):
        '''Numpy data-type of the data array.

    .. versionadded:: 2.0 
    
    **Examples:**
    
    >>> c.dtype
    dtype('float64')
    >>> import numpy
    >>> c.dtype = numpy.dtype('float32')

        '''
        data = self.get_data(None)
        if data is not None:
            return data.dtype

        bounds = self.get_bounds(None)
        if bounds is not None:
            return bounds.dtype

        raise AttributeError("{} doesn't have attribute 'dtype'".format(
            self.__class__.__name__))
    @dtype.setter
    def dtype(self, value):
        data = self.get_data(None)
        if data is not None:
            data.dtype = value

        bounds = self.get_bounds(None)
        if bounds is not None:
            bounds.dtype = value


    @property
    def isperiodic(self): 
        '''

    .. versionadded:: 2.0 
    
    >>> print(c.period())
    None
    >>> c.isperiodic
    False
    >>> print(c.period(cf.Data(360, 'degeres_east')))
    None
    >>> c.isperiodic
    True
    >>> c.period(None)
    <CF Data(): 360 degrees_east>
    >>> c.isperiodic
    False
    
    '''
        return self._custom.get('period', None) is not None


    @property
    def lower_bounds(self):
        '''The lower bounds of cells.

    If there are no cell bounds then the coordinates are used as the
    lower bounds.
    
    .. versionadded:: 2.0 
    
    .. seealso:: `upper_bounds`
    
    **Examples:**
    
    >>> print(c.array)
    [4  2  0]
    >>> print(c.bounds.array)
    [[ 5  3]
     [ 3  1]
     [ 1 -1]]
    >>> c.lower_bounds
    <CF Data(3): [3, 1, -1]>
    >>> b = c.del_bounds()
    >>> c.lower_bounds
    <CF Data(3): [4, 2, 0]>

        '''
        data = self.get_bounds_data(None)
        if data is not None:            
            out = data.min(-1)
            out.squeeze(-1, inplace=True)
            return out
        else:
            data = self.get_data(None)
            if data is not None:
                return data.copy()
        #--- End: if
                
        raise AttributeError(
            "Can't get lower bounds when there are no bounds nor coordinate data")


    @property
    def Units(self):
        '''The `cf.Units` object containing the units of the data array.

    Stores the units and calendar CF properties in an internally
    consistent manner. These are mirrored by the `units` and
    `calendar` CF properties respectively.
    
    **Examples:**
    
    >>> f.Units
    <Units: K>
    
    >>> f.Units
    <Units: days since 2014-1-1 calendar=noleap>

        '''
        return super().Units
    @Units.setter
    def Units(self, value):
        PropertiesData.Units.fset(self, value)

        # Set the Units on the bounds
        bounds = self.get_bounds(None)
        if bounds is not None:
            bounds.Units = value

        # Set the Units on the period
        period = self._custom.get('period')
        if period is not None:
            period = period.copy()
            period.Units = value
            self._custom['period'] = period
    @Units.deleter
    def Units(self):
        PropertiesData.Units.fdel(self)

    @property
    def upper_bounds(self):
        '''The upper bounds of cells.

    If there are no cell bounds then the coordinates are used as the
    upper bounds.
    
    .. versionadded:: 2.0 
    
    .. seealso:: `lower_bounds`
    
    **Examples:**
    
    >>> print(c.array)
    [4  2  0]
    >>> print(c.bounds.array)
    [[ 5  3]
     [ 3  1]
     [ 1 -1]]
    >>> c.upper_bounds
    <CF Data(3): [5, 3, 1]>
    >>> b = c.del_bounds()
    >>> c.upper_bounds
    <CF Data(3): [4, 2, 0]>

        '''
        data = self.get_bounds_data(None)
        if data is not None:            
            out = data.max(-1)
            out.squeeze(-1, inplace=True)
            return out
        else:
            data = self.get_data(None)
            if data is not None:
                return data.copy()
        #--- End: if
        
        raise AttributeError(
            "Can't get upper bounds when there are no bounds nor coordinate data")


    def mask_invalid(self, inplace=False, i=False):
        '''Mask the array where invalid values occur.

    Note that:
    
    * Invalid values are Nan or inf
    
    * Invalid values in the results of arithmetic operations only
      occur if the raising of `FloatingPointError` exceptions has been
      suppressed by `cf.Data.seterr`.
    
    * If the raising of `FloatingPointError` exceptions has been
      allowed then invalid values in the results of arithmetic
      operations it is possible for them to be automatically converted
      to masked values, depending on the setting of
      `cf.Data.mask_fpe`. In this case, such automatic conversion
      might be faster than calling `mask_invalid`.
    
    .. seealso:: `cf.Data.mask_fpe`, `cf.Data.seterr`
    
    :Parameters:
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with masked elements.
    
    **Examples:**
    
    >>> print(f.array)
    [ 0.  1.]
    >>> print(g.array)
    [ 1.  2.]
    
    >>> old = cf.data.seterr('ignore')
    >>> h = g/f
    >>> print(h.array)
    [ inf   2.]
    >>> h.mask_invalid(inplace=True)
    >>> print(h.array)
    [--  2.]
    
    >>> h = g**12345
    >>> print(h.array)
    [ 1.  inf]
    >>> h.mask_invalid(inplace=True)
    >>> print(h.array)
    [1.  --]
    
    >>> old = cf.data.seterr('raise')
    >>> old = cf.data.mask_fpe(True)
    >>> print((g/f).array)
    [ --  2]
    >>> print((g**12345).array)
    [1.  -- ]

        '''
        # Set bounds to True to bypass 'if bounds' check in call:
        return self._apply_data_operation(
            'mask_invalid', bounds=True, inplace=inplace, i=i)


    # ----------------------------------------------------------------
    # Attribute
    # ----------------------------------------------------------------
    @property
    def dtype(self):
        '''The `numpy` data type of the data array.

By default this is the data type with the smallest size and smallest
scalar kind to which all sub-arrays of the master data array may be
safely cast without loss of information. For example, if the
sub-arrays have data types 'int64' and 'float32' then the master data
array's data type will be 'float64'; or if the sub-arrays have data
types 'int64' and 'int32' then the master data array's data type will
be 'int64'.

Setting the data type to a `numpy.dtype` object, or any object
convertible to a `numpy.dtype` object, will cause the master data
array elements to be recast to the specified type at the time that
they are next accessed, and not before. This does not immediately
change the master data array elements, so, for example, reinstating
the original data type prior to data access results in no loss of
information.

Deleting the data type forces the default behaviour. Note that if the
data type of any sub-arrays has changed after `dtype` has been set
(which could occur if the data array is accessed) then the reinstated
default data type may be different to the data type prior to `dtype`
being set.

**Examples:**

>>> f.dtype
dtype('float64')
>>> type(f.dtype)
<type 'numpy.dtype'>

>>> print(f.array)
[0.5 1.5 2.5]
>>> import numpy
>>> f.dtype = numpy.dtype(int)
>>> print(f.array)
[0 1 2]
>>> f.dtype = bool
>>> print(f.array)
[False  True  True]
>>> f.dtype = 'float64'
>>> print(f.array)
[ 0.  1.  1.]

>>> print(f.array)
[0.5 1.5 2.5]
>>> f.dtype = int
>>> f.dtype = bool
>>> f.dtype = float
>>> print(f.array)
[ 0.5  1.5  2.5]

        '''
        try:
            return super().dtype
        except AttributeError as error:
            bounds = self.get_bounds(None)
            if bounds is not None:
                return bounds.dtype
            
            raise AttributeError(error)

    @dtype.setter
    def dtype(self, value):
        # DCH - allow dtype to be set before data c.f.  Units
        data = self.get_data(None)
        if data is not None:
            self.Data.dtype = value

    @dtype.deleter
    def dtype(self):
        data = self.get_data(None)
        if data is not None:
            del self.Data.dtype


    # ----------------------------------------------------------------
    # Methods
    # ----------------------------------------------------------------
    def ceil(self, bounds=True, inplace=False, i=False):
        '''The ceiling of the data, element-wise.

    The ceiling of ``x`` is the smallest integer ``n``, such that
     ``n >= x``.
    
    .. versionadded:: 1.0
    
    .. seealso:: `floor`, `rint`, `trunc`
    
    :Parameters:
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with ceilinged of data. If the operation was
            in-place then `None` is returned.
    
    **Examples:**
    
    >>> print(f.array)
    [-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
    >>> print(f.ceil().array)
    [-1. -1. -1. -1.  0.  1.  2.  2.  2.]
    >>> f.ceil(inplace=True)
    >>> print(f.array)
    [-1. -1. -1. -1.  0.  1.  2.  2.  2.]

        '''
        return self._apply_data_operation(
            'ceil', bounds=bounds, inplace=inplace, i=i)


    def chunk(self, chunksize=None):
        '''Partition the data array.

    :Parameters:
    
        chunksize: `int`, optional
            Set the new chunksize, in bytes.
    
    :Returns:
    
        `None`
    
    **Examples:**
    
    >>> c.chunksize()
    
    >>> c.chunksize(1e8)

        '''
        super().chunk(chunksize)

        # Chunk the bounds, if they exist.
        bounds = self.get_bounds(None)
        if bounds is not None:
            bounds.chunk(chunksize)

            
    def clip(self, a_min, a_max, units=None, bounds=True,
             inplace=False, i=False):
        '''Limit the values in the data.

    Given an interval, values outside the interval are clipped to the
    interval edges. For example, if an interval of ``[0, 1]`` is
    specified, values smaller than 0 become 0, and values larger than
    1 become 1.
    
    :Parameters:
     
        a_min:
            Minimum value. If `None`, clipping is not performed on
            lower interval edge. Not more than one of `a_min` and
            `a_max` may be `None`.
    
        a_max:
            Maximum value. If `None`, clipping is not performed on
            upper interval edge. Not more than one of `a_min` and
            `a_max` may be `None`.
    
        units: `str` or `Units`
            Specify the units of *a_min* and *a_max*. By default the
            same units as the data are assumed.
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any bounds
            are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns: 
    
            The construct with clipped data. If the operation was
            in-place then `None` is returned.
    
    **Examples:**
    
    >>> g = f.clip(-90, 90)
    >>> g = f.clip(-90, 90, 'degrees_north')

        '''
        return self._apply_data_operation(
            'clip', a_min, a_max, bounds=bounds, inplace=inplace, i=i,
            units=units)

    
    def close(self):
        '''Close all files referenced by the construct.

    Note that a closed file will be automatically re-opened if its
    contents are subsequently required.
    
    .. seealso:: `files`
    
    :Returns:
    
        `None`
    
    **Examples:**
    
    >> c.close()

        '''
        super().close()

        bounds = self.get_bounds(None)
        if bounds is not None:
            bounds.close()


    @classmethod
    def concatenate(cls, variables, axis=0, _preserve=True):
        '''Join a sequence of variables together.
    
    :Parameters:
    
        variables: sequence of constructs
    
        axis: `int`, optional
    
    :Returns:
    
        TODO
        '''
        variable0 = variables[0]

        if len(variables) == 1:
            return variable0.copy()
        
        out = super().concatenate(variables, axis=axis, _preserve=_preserve)

        bounds = variable0.get_bounds(None)
        if bounds is not None:
            bounds = bounds.concatenate([v.get_bounds() for v in variables],
                                        axis=axis,
                                        _preserve=_preserve)
            out.set_bounds(bounds, copy=False)

        return out


    def cos(self, bounds=True, inplace=False,  i=False):
        '''Take the trigonometric cosine of the data, element-wise.

    Units are accounted for in the calculation, so that the cosine
    of 90 degrees_east is 0.0, as is the cosine of 1.57079632
    radians. If the units are not equivalent to radians (such as
    Kelvin) then they are treated as if they were radians.

    The output units are '1' (nondimensional).
    
    .. seealso:: `sin`, `tan`
    
    :Parameters:
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with the cosine of data values. If the
            operation was in-place then `None` is returned.
    
    **Examples:**
    
    >>> f.Units
    <Units: degrees_east>
    >>> print(f.array)
    [[-90 0 90 --]]
    >>> f.cos()
    >>> f.Units
    <Units: 1>
    >>> print(f.array)
    [[0.0 1.0 0.0 --]]
    
    >>> f.Units
    <Units: m s-1>
    >>> print(f.array)
    [[1 2 3 --]]
    >>> f.cos()
    >>> f.Units
    <Units: 1>
    >>> print(f.array)
    [[0.540302305868 -0.416146836547 -0.9899924966 --]]

        '''
        return self._apply_data_operation(
            'cos', bounds=bounds, inplace=inplace, i=i)


    def cyclic(self, axes=None, iscyclic=True):
        '''Set the cyclicity of axes of the data array.

    .. seealso:: `iscyclic`
    
    :Parameters:
    
        axes: (sequence of) `int`
            The axes to be set. Each axis is identified by its integer
            position. By default no axes are set.
            
        iscyclic: `bool`, optional
            If False then the axis is set to be non-cyclic. By default
            the axis is set to be cyclic.
    
    :Returns:
    
        `set`
    
    **Examples:**
    
        TODO

        '''
        out = super().cyclic(axes, iscyclic)

        if axes is None:
            return out

        bounds = self.get_bounds(None)
        if bounds is not None:
            axes = self._parse_axes(axes)
            bounds.cyclic(axes, iscyclic)
        
        return out

            
    def equivalent(self, other, rtol=None, atol=None, traceback=False):
        '''True if two constructs are equal, False otherwise.

    Two real numbers ``x`` and ``y`` are considered equal if
    ``|x-y|<=atol+rtol|y|``, where ``atol`` (the tolerance on absolute
    differences) and ``rtol`` (the tolerance on relative differences)
    are positive, typically very small numbers. See the *atol* and
    *rtol* parameters.
    
    :Parameters:
    
        other: 
            The object to compare for equality.
    
    
        atol: `float`, optional
            The tolerance on absolute differences between real
            numbers. The default value is set by the `ATOL` function.
    
        rtol: `float`, optional
            The tolerance on relative differences between real
            numbers. The default value is set by the `RTOL` function.

        '''     
        if self is other:
            return True

        # Check that each instance is the same type
        if type(self) != type(other):
            print("{}: Different types: {}, {}".format(
                self.__class__.__name__,
                self.__class__.__name__,
                other.__class__.__name__))
            return False
       
        identity0 = self.identity()
        identity1 = other.identity()

        if identity0 is None or identity1 is None or identity0 != identity1:
            # add traceback
            return False
                  
        # ------------------------------------------------------------
        # Check the special attributes
        # ------------------------------------------------------------
        self_special  = self._private['special_attributes']
        other_special = other._private['special_attributes']
        if set(self_special) != set(other_special):
            if traceback:
                print("%s: Different attributes: %s" %
                      (self.__class__.__name__,
                       set(self_special).symmetric_difference(other_special)))
            return False

        for attr, x in self_special.items():
            y = other_special[attr]

            result = cf_equivalent(x, y, rtol=rtol, atol=atol,
                                   traceback=traceback)
               
            if not result:
                if traceback:
                    print("{}: Different {} attributes: {!r}, {!r}".format(
                        self.__class__.__name__, attr, x, y))
                return False
        #--- End: for

        # ------------------------------------------------------------
        # Check the data
        # ------------------------------------------------------------
        if not self._equivalent_data(other, rtol=rtol, atol=atol,
                                     traceback=traceback):
            # add traceback
            return False
            
        return True
    

    def contiguous(self, overlap=True):
        '''Return True if a construct has contiguous cells.

    A construct is contiguous if its cell boundaries match up, or
    overlap, with the boundaries of adjacent cells.
    
    In general, it is only possible for a zero, 1 or 2 dimensional
    construct with bounds to be contiguous. A size 1 construct with
    any number of dimensions is always contiguous.
    
    An exception occurs if the construct is multdimensional and has
    more than one element.
    
    .. versionadded:: 2.0 
    
    :Parameters:
    
        overlap : bool, optional    
            If False then overlapping cell boundaries are not
            considered contiguous. By default cell boundaries are
            considered contiguous.
    
    :Returns:
    
        `bool`
            Whether or not the construct's cells are contiguous.
    
    **Examples:**
    
    >>> c.has_bounds()
    False
    >>> c.contiguous()
    False
    
    >>> print(c.bounds[:, 0])
    [  0.5   1.5   2.5   3.5 ]
    >>> print(c.bounds[:, 1])
    [  1.5   2.5   3.5   4.5 ]
    >>> c.contiuous()
    True
    
    >>> print(c.bounds[:, 0])
    [  0.5   1.5   2.5   3.5 ]
    >>> print(c.bounds[:, 1])
    [  2.5   3.5   4.5   5.5 ]
    >>> c.contiuous()
    True
    >>> c.contiuous(overlap=False)
    False

        '''
        bounds = self.get_bounds(None)
        if bounds is None:
            return False

        return bounds.contiguous(overlap=overlap, direction=self.direction())

#        if monoyine:
#            return self.monit()#
#
#        return False


    def convert_reference_time(self, units=None,
                               calendar_months=False,
                               calendar_years=False, inplace=False,
                               i=False):
        '''Convert reference time data values to have new units.

    Conversion is done by decoding the reference times to date-time
    objects and then re-encoding them for the new units.
    
    Any conversions are possible, but this method is primarily for
    conversions which require a change in the date-times originally
    encoded. For example, use this method to reinterpret data values
    in units of "months" since a reference time to data values in
    "calendar months" since a reference time. This is often necessary
    when units of "calendar months" were intended but encoded as
    "months", which have special definition. See the note and examples
    below for more details.
    
    For conversions which do not require a change in the date-times
    implied by the data values, this method will be considerably
    slower than a simple reassignment of the units. For example, if
    the original units are ``'days since 2000-12-1'`` then ``c.Units =
    cf.Units('days since 1901-1-1')`` will give the same result and be
    considerably faster than ``c.convert_reference_time(cf.Units('days
    since 1901-1-1'))``.
    
    .. note:: It is recommended that the units "year" and "month" be
              used with caution, as explained in the following excerpt
              from the CF conventions: "The Udunits package defines a
              year to be exactly 365.242198781 days (the interval
              between 2 successive passages of the sun through vernal
              equinox). It is not a calendar year. Udunits includes
              the following definitions for years: a common_year is
              365 days, a leap_year is 366 days, a Julian_year is
              365.25 days, and a Gregorian_year is 365.2425 days. For
              similar reasons the unit ``month``, which is defined to
              be exactly year/12, should also be used with caution.
    
    :Parameters:
    
        units: `Units`, optional
            The reference time units to convert to. By default the
            units days since the original reference time in the
            original calendar.
    
            *Parameter example:*
              If the original units are ``'months since 2000-1-1'`` in
              the Gregorian calendar then the default units to convert
              to are ``'days since 2000-1-1'`` in the Gregorian
              calendar.
    
        calendar_months: `bool`, optional
            If True then treat units of ``'months'`` as if they were
            calendar months (in whichever calendar is originally
            specified), rather than a 12th of the interval between 2
            successive passages of the sun through vernal equinox
            (i.e. 365.242198781/12 days).
    
        calendar_years: `bool`, optional
            If True then treat units of ``'years'`` as if they were
            calendar years (in whichever calendar is originally
            specified), rather than the interval between 2 successive
            passages of the sun through vernal equinox
            (i.e. 365.242198781 days).
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns: 
    
            The construct with converted reference time data values.
    
    **Examples:**
    
    >>> print(f.array)
    [1  2  3  4]
    >>> f.Units
    <Units: months since 2000-1-1>
    >>> print(f.datetime_array)
    [datetime.datetime(2000, 1, 31, 10, 29, 3, 831197) TODO
     datetime.datetime(2000, 3, 1, 20, 58, 7, 662441)
     datetime.datetime(2000, 4, 1, 7, 27, 11, 493645)
     datetime.datetime(2000, 5, 1, 17, 56, 15, 324889)]
    >>> f.convert_reference_time(calendar_months=True, inplace=True)
    >>> print(f.datetime_array)
    [datetime.datetime(2000, 2, 1, 0, 0) TODOx
     datetime.datetime(2000, 3, 1, 0, 0)
     datetime.datetime(2000, 4, 1, 0, 0)
     datetime.datetime(2000, 5, 1, 0, 0)]
    >>> print(f.array)
    [  31.   60.   91.  121.]
    >>> f.Units
    <Units: days since 2000-1-1>

        '''
        return self._apply_data_operation(
            'convert_reference_time', inplace=inplace, i=i, units=units,
            calendar_months=calendar_months, calendar_years=calendar_years)

    
    def flatten(self, axes=None, inplace=False):
        '''Flatten axes of the data

    Any subset of the axes may be flattened.

    The shape of the data may change, but the size will not.

    The flattening is executed in row-major (C-style) order. For
    example, the array ``[[1, 2], [3, 4]]`` would be flattened across
    both dimensions to ``[1 2 3 4]``.

    .. versionaddedd:: 3.0.2

    .. seealso:: `insert_dimension`, `flip`, `swapaxes`, `transpose`

    :Parameters:
   
        axes: (sequence of) int or str, optional
            Select the axes.  By default all axes are flattened. The
            *axes* argument may be one, or a sequence, of:
    
              * An internal axis identifier. Selects this axis.
            ..
    
              * An integer. Selects the axis coresponding to the given
                position in the list of axes of the data array.
    
            No axes are flattened if *axes* is an empty sequence.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
    :Returns:

            The construct with flattened data, or `None` if the
            operation was in-place.

    **Examples**

    >>> f.shape
    (1, 2, 3, 4)
    >>> f.flatten().shape
    (24,)
    >>> f.flatten([1, 3]).shape
    (1, 8, 3)
    >>> f.flatten([0, -1], inplace=True)
    >>> f.shape
    (4, 2, 3)

        '''
        # Note the 'axes' argument can change mid-method meaning it is not
        # possible to consolidate this method using a call to
        # _apply_data_operations, despite having mostly the same logic.
        v = super().flatten(axes, inplace=inplace)
        if inplace:
            v = self
            
        bounds = v.get_bounds(None)
        if bounds is not None:
            axes = self._parse_axes(axes)
            bounds.flatten(axes, inplace=True)
        
        if inplace:
            v = None
        return v


    def floor(self, bounds=True, inplace=False, i=False):
        '''Floor the data array, element-wise.

    The floor of ``x`` is the largest integer ``n``, such that ``n <= x``.
    
    .. versionadded:: 1.0
    
    .. seealso:: `ceil`, `rint`, `trunc`
    
    :Parameters:
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
            
            The construct with floored data. If the operation was
            in-place then `None` is returned.
    
    **Examples:**
    
    >>> print(f.array)
    [-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
    >>> print(f.floor().array)
    [-2. -2. -2. -1.  0.  1.  1.  1.  1.]
    >>> f.floor(inplace=True)
    >>> print(f.array)
    [-2. -2. -2. -1.  0.  1.  1.  1.  1.]

        '''
        return self._apply_data_operation(
            'floor', bounds=bounds, inplace=inplace, i=i)


    def direction(self):
        '''Return None, indicating that it is not specified whether the
    values are increasing or decreasing.
    
    .. versionadded:: 2.0 
    
    :Returns:
    
        None
            
    **Examples:**
    
    >>> print(c.direction())
    None
    
            ''' 
        return


    def match_by_property(self, *mode, **properties):
        '''Determine whether or not a variable satisfies conditions.

    Conditions may be specified on the variable's attributes and CF
    properties.
    
    :Parameters:
     
    :Returns:
    
        out: `bool`
            Whether or not the variable matches the given criteria.
    
    **Examples:**

    TODO

        '''
        _or = False
        if mode:
            if len(mode) > 1:
                raise ValueError("Can provide at most one positional argument")
            
            x = mode[0]
            if x == 'or':
                _or = True
            elif x != 'and':
                raise ValueError(
                    "Positional argument, if provided, must one of 'or', 'and'")
        #--- End: if

        if not properties:
            return True

        self_properties = self.properties()        

        ok = True
        for name, value0 in properties.items():
            value1 = self_property.get(name)
            ok = self._matching_values(value0, value1, units=(name=='units'))
            
            if _or:
                if ok:
                    break
            elif not ok:
                break
        #--- End: for

        return ok


    def match_by_identity(self, *identities):
        '''Determine whether or not a variable satisfies conditions.

    Conditions may be specified on the variable's attributes and CF
    properties.
    
    :Parameters:
    
    :Returns:
    
        `bool`
            Whether or not the variable matches the given criteria.
    
    **Examples:**

        TODO

        '''
        # Return all constructs if no identities have been provided
        if not identities:
            return True

        identities = self.identities()
        
        ok = False
        for value0 in identities:          
            for value1 in self_identities:
                ok = self._matching_values(value0, value1)
                if ok:
                    break
            #--- End: for

            if ok:
                break
        #--- End: for

        return ok


    def override_calendar(self, calendar, inplace=False,  i=False):
        '''Override the calendar of date-time units.

    The new calendar **need not** be equivalent to the original one
    and the data array elements will not be changed to reflect the new
    units. Therefore, this method should only be used when it is known
    that the data array values are correct but the calendar has been
    incorrectly encoded.
    
    Not to be confused with setting the `calendar` or `Units`
    attributes to a calendar which is equivalent to the original
    calendar
    
    .. seealso:: `calendar`, `override_units`, `units`, `Units`
    
    :Parameters:
    
        calendar: `str`
            The new calendar.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
    TODO
    
    **Examples:**
    
    TODO
    
    >>> g = f.override_calendar('noleap')

        '''
        return self._apply_data_operation(
            'override_calendar', calendar, inplace=inplace, i=i)


    def override_units(self, units, inplace=False, i=False):
        '''Override the units.

    The new units need not be equivalent to the original ones, and the
    data array elements will not be changed to reflect the new
    units. Therefore, this method should only be used when it is known
    that the data array values are correct but the units have
    incorrectly encoded.
    
    Not to be confused with setting the `units` or `Units` attribute
    to units which are equivalent to the original units.
    
    .. seealso:: `calendar`, `override_calendar`, `units`, `Units`
    
    :Parameters:
    
        units: `str` or `Units`
            The new units for the data array.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            TODO
    
    **Examples:**
    
    >>> f.Units
    <Units: hPa>
    >>> f.datum(0)
    100000.0
    >>> f.override_units('km')
    >>> f.Units
    <Units: km>
    >>> f.datum(0)
    100000.0
    >>> f.override_units(Units('watts'))
    >>> f.Units
    <Units: watts>
    >>> f.datum(0)
    100000.0

        '''
        return self._apply_data_operation(
            'override_units', units, inplace=inplace, i=i)


    def files(self):
        '''Return the names of any files containing parts of the data array.

    .. seealso:: `close`
    
    :Returns:
    
        `set`
            The file names in normalized, absolute form.
    
    **Examples:**
    
    >>> c.files()
    {'/data/user/file1.nc',
     '/data/user/file2.nc',
     '/data/user/file3.nc'}
    >>> a = c.array
    >>> f.files()
    set()

        '''
        out = super().files()

        bounds = self.get_bounds(None)
        if bounds is not None:
            out.update(bounds.files())

        return out


    def flip(self, axes=None, inplace=False, i=False):
        '''Flip (reverse the direction of) data dimensions.

    .. seealso:: `insert_dimension`, `squeeze`, `transpose`, `unsqueeze`
    
    :Parameters:
    
        axes: optional
           Select the domain axes to flip. One, or a sequence, of:
    
              * The position of the dimension in the data.
    
            If no axes are specified then all axes are flipped.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use the *inplace* parameter instead.
    
    :Returns:
    
            The construct with flipped axes, or `None` if the operation
            was in-place.
    
    **Examples:**
    
    >>> f.flip()
    >>> f.flip(1)
    >>> f.flip([0, 1])
    
    >>> g = f[::-1, :, ::-1]
    >>> f.flip([2, 0]).equals(g)
    True

        '''
        if i:
            _DEPRECATION_ERROR_KWARGS(self, 'flip', i=True) # pragma: no cover

        v = super().flip(axes=axes, inplace=inplace)
        if inplace:
            v = self

        bounds = v.get_bounds(None)
        if bounds is not None:
            # --------------------------------------------------------
            # Flip the bounds.
            #
            # As per section 7.1 in the CF conventions: i) if the
            # variable is 0 or 1 dimensional then flip all dimensions
            # (including the trailing size 2 dimension); ii) if
            # the variable has 2 or more dimensions then do not flip
            # the trailing dimension.
            # --------------------------------------------------------
            if not v.ndim:
                # Flip the bounds of a 0-d variable
                axes = (0,)
            elif v.ndim == 1:
                # Flip the bounds of a 1-d variable
                if axes in (0, 1):
                    axes = (0, 1)
                elif axes is not None:
                    axes = v._parse_axes(axes) + [-1]
            else:
                # Do not flip the bounds of an N-d variable (N >= 2)
                axes = v._parse_axes(axes)

            bounds.flip(axes, inplace=True)

        if inplace:
            v = None            
        return v


    def exp(self, bounds=True, inplace=False, i=False):
        '''The exponential of the data, element-wise.

    .. seealso:: `log`
    
    :Parameters:
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with the exponential of data values. If the
            operation was in-place then `None` is returned.
    
    **Examples:**
    
    >>> f.data
    <CF Data(1, 2): [[1, 2]]>
    >>> f.exp().data            
    <CF Data(1, 2): [[2.71828182846, 7.38905609893]]>
    
    >>> f.data
    <CF Data(1, 2): [[1, 2]] 2>
    >>> f.exp().data            
    <CF Data(1, 2): [[7.38905609893, 54.5981500331]]>
    
    >>> f.data
    <CF Data(1, 2): [[1, 2]] kg m-1 s-2>
    >>> f.exp()          
    ValueError: Can't take exponential of dimensional quantities: <Units: kg m-1 s-2>

        '''
        return self._apply_data_operation(
            'exp', bounds=bounds, inplace=inplace, i=i)


    def set_bounds(self, bounds, copy=True):
        '''Set the bounds.

    .. versionadded:: 3.0.0
    
    .. seealso: `del_bounds`, `get_bounds`, `has_bounds`, `set_data`
    
    :Parameters:
    
        bounds: `Bounds`
            The bounds to be inserted.
    
        copy: `bool`, optional
            If False then do not copy the bounds prior to
            insertion. By default the bounds are copied.
    
    :Returns:
    
        `None`
    
    **Examples:**
    
    >>> import numpy
    >>> b = cfdm.Bounds(data=cfdm.Data(numpy.arange(10).reshape(5, 2)))
    >>> c.set_bounds(b)
    >>> c.has_bounds()
    True
    >>> c.get_bounds()
    <Bounds: (5, 2) >
    >>> b = c.del_bounds()
    >>> b
    <Bounds: (5, 2) >
    >>> c.has_bounds()
    False
    >>> print(c.get_bounds(None))
    None
    >>> print(c.del_bounds(None))
    None

        '''
        data = self.get_data(None)

        if data is not None and bounds.shape[:data.ndim] != data.shape:
            # Check shape
            raise ValueError(
                "Can't set bounds: Incorrect shape: {0})".format(bounds.shape))

        if copy:            
            bounds = bounds.copy()

        # Check units
        units      = bounds.Units
        self_units = self.Units

        if units and not units.equivalent(self_units):
            raise ValueError(
                "Can't set bounds: Bounds units of {!r} are not equivalent to {!r}".format(
                    bounds.Units, self.Units))
        
            bounds.Units = self_units
            
        if not units:        
           bounds.override_units(self_units, inplace=True)
        
        # Copy selected properties to the bounds
        #for prop in ('standard_name', 'axis', 'positive',
        #             'leap_months', 'leap_years', 'month_lengths'):
        #    value = self.get_property(prop, None)
        #    if value is not None:
        #        bounds.set_property(prop, value)

        
        self._custom['direction'] = None
        
        super().set_bounds(bounds, copy=False)


    def sin(self, bounds=True, inplace=False, i=False):
        '''The trigonometric sine of the data, element-wise.

    Units are accounted for in the calculation. For example, the
    sine of 90 degrees_east is 1.0, as is the sine of 1.57079632
    radians. If the units are not equivalent to radians (such as
    Kelvin) then they are treated as if they were radians.
    
    The Units are changed to '1' (nondimensional).
    
    .. seealso:: `cos`, `tan`
    
    :Parameters:
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with the sine of data values. If the
            operation was in-place then `None` is returned.
    
    **Examples:**
    
    >>> f.Units
    <Units: degrees_north>
    >>> print(f.array)
    [[-90 0 90 --]]
    >>> f.sin()
    >>> f.Units
    <Units: 1>
    >>> print(f.array)
    [[-1.0 0.0 1.0 --]]
    
    >>> f.Units
    <Units: m s-1>
    >>> print(f.array)
    [[1 2 3 --]]
    >>> f.sin()
    >>> f.Units
    <Units: 1>
    >>> print(f.array)
    [[0.841470984808 0.909297426826 0.14112000806 --]]

        '''
        return self._apply_data_operation(
            'sin', bounds=bounds, inplace=inplace, i=i)


    def arctan(self, bounds=True, inplace=False):
        '''Take the trigonometric inverse tangent of the data element-wise.

    Units are ignored in the calculation. The result has units of radians.

    The "standard_name" and "long_name" properties are removed from
    the result.

    .. versionadded:: 3.0.7

    .. seealso:: `tan`
    
    :Parameters:
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
    :Returns:
    
            The construct with the trigonometric inverse tangent of data
            values. If the operation was in-place then `None` is returned.
    
    **Examples:**
    
    >>> d = cf.Data([[0, 1, 2], [3, -99, 5]], mask=[[0, 0, 0], [0, 1, 0]])
    >>> print(d.array)
    [[0  1 2]
     [3 -- 5]]
    >>> e = d.arctan()
    >>> e
    <CF Data(2, 3): [[0.0, ..., 1.373400766945016]] radians>
    >>> print(e.array)
    [[0.0                0.7853981633974483 1.1071487177940904]
     [1.2490457723982544                 -- 1.373400766945016 ]]

        '''
        return self._apply_data_operation(
            'arctan', bounds=bounds, inplace=inplace)


    def arcsinh(self, bounds=True, inplace=False):
        '''Take the inverse hyperbolic sine of the data element-wise.

    Units are ignored in the calculation. The result has units of radians.

    The "standard_name" and "long_name" properties are removed from
    the result.

    .. versionadded:: 3.1.0

    .. seealso:: `sinh`

    :Parameters:

        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.

    :Returns:
    
            The construct with the inverse hyperbolic sine of data values.
            If the operation was in-place then `None` is returned.

    **Examples:**

    >>> d = cf.Data([[0, 1, 2], [3, -99, 5]], mask=[[0, 0, 0], [0, 1, 0]])
    >>> print(d.array)
    [[0  1 2]
     [3 -- 5]]
    >>> e = d.arcsinh()
    >>> e
    <CF Data(2, 3): [[0.0, ..., 2.3124383412727525]] radians>
    >>> print(e.array)
    [[0.0 0.881373587019543 1.4436354751788103]
     [1.8184464592320668 -- 2.3124383412727525]]

        '''
        return self._apply_data_operation(
            'arcsinh', bounds=bounds, inplace=inplace)


    def tanh(self, bounds=True, inplace=False):
        '''Take the hyperbolic tangent of the data array.

    Units are accounted for in the calculation. If the units are not
    equivalent to radians (such as Kelvin) then they are treated as if
    they were radians. For example, the the hyperbolic tangent of 90
    degrees_east is 0.91715234, as is the hyperbolic tangent of
    1.57079632 radians.

    The output units are changed to '1' (nondimensional).

    The "standard_name" and "long_name" properties are removed from
    the result.

    .. versionadded:: 3.1.0

    .. seealso:: `sinh`, `cosh`


    :Parameters:

        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.

    :Returns:
    
            The construct with the hyperbolic tangent of data values. If the
            operation was in-place then `None` is returned.

    **Examples:**

    >>> d.Units
    <Units: degrees_north>
    >>> print(d.array)
    [[-90 0 90 --]]
    >>> e = d.tanh()
    >>> e.Units
    <Units: 1>
    >>> print(e.array)
    [[-0.9171523356672744 0.0 0.9171523356672744 --]]

    >>> d.Units
    <Units: m s-1>
    >>> print(d.array)
    [[1 2 3 --]]
    >>> d.tanh(inplace=True)
    >>> d.Units
    <Units: 1>
    >>> print(d.array)
    [[0.7615941559557649 0.9640275800758169 0.9950547536867305 --]]

        '''
        return self._apply_data_operation(
            'tanh', bounds=bounds, inplace=inplace)


    def sinh(self, bounds=True, inplace=False):
        '''Take the hyperbolic sine of the data array in place.

    Units are accounted for in the calculation. If the units are not
    equivalent to radians (such as Kelvin) then they are treated as if
    they were radians. For example, the the hyperbolic sine of 90
    degrees_north is 2.30129890, as is the hyperbolic sine of
    1.57079632 radians.

    The output units are changed to '1' (nondimensional).

    The "standard_name" and "long_name" properties are removed from
    the result.

    .. versionadded:: 3.1.0

    .. seealso:: `arcsinh`, `cosh`, `tanh`

    :Parameters:

        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.

    :Returns:
    
            The construct with the hyperbolic sine of data values. If the
            operation was in-place then `None` is returned.

    **Examples:**

    >>> d.Units
    <Units: degrees_north>
    >>> print(d.array)
    [[-90 0 90 --]]
    >>> d.sinh(inplace=True)
    >>> d.Units
    <Units: 1>
    >>> print(d.array)
    [[-2.3012989023072947 0.0 2.3012989023072947 --]]

    >>> d.Units
    <Units: m s-1>
    >>> print(d.array)
    [[1 2 3 --]]
    >>> d.sinh(inplace=True)
    >>> d.Units
    <Units: 1>
    >>> print(d.array)
    [[1.1752011936438014 3.626860407847019 10.017874927409903 --]]

        '''
        return self._apply_data_operation(
            'sinh', bounds=bounds, inplace=inplace)


    def cosh(self, bounds=True, inplace=False):
        '''Take the hyperbolic cosine of the data array in place.

    Units are accounted for in the calculation. If the units are not
    equivalent to radians (such as Kelvin) then they are treated as if
    they were radians. For example, the the hyperbolic cosine of 0
    degrees_east is 1.0, as is the hyperbolic cosine of 1.57079632 radians.

    The output units are changed to '1' (nondimensional).

    The "standard_name" and "long_name" properties are removed from
    the result.

    .. versionadded:: 3.1.0

    .. seealso:: `sinh`, `tanh`

    :Parameters:

        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.

    :Returns:
    
            The construct with the hyperbolic cosine of data values. If the
            operation was in-place then `None` is returned.

    **Examples:**

    >>> d.Units
    <Units: degrees_north>
    >>> print(d.array)
    [[-90 0 90 --]]
    >>> e = d.cosh()
    >>> e.Units
    <Units: 1>
    >>> print(e.array)
    [[2.5091784786580567 1.0 2.5091784786580567 --]]

    >>> d.Units
    <Units: m s-1>
    >>> print(d.array)
    [[1 2 3 --]]
    >>> d.cosh(inplace=True)
    >>> d.Units
    <Units: 1>
    >>> print(d.array)
    [[1.5430806348152437 3.7621956910836314 10.067661995777765 --]]

        '''
        return self._apply_data_operation(
            'cosh', bounds=bounds, inplace=inplace)


    def tan(self, bounds=True, inplace=False, i=False):
        '''The trigonometric tangent of the data, element-wise.

    Units are accounted for in the calculation, so that the
    tangent of 180 degrees_east is 0.0, as is the tangent of
    3.141592653589793 radians. If the units are not equivalent to
    radians (such as Kelvin) then they are treated as if they were
    radians.
    
    The Units are changed to '1' (nondimensional).
    
    .. seealso:: `arctan`, `cos`, `sin`
    
    :Parameters:
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
    :Returns:
            
            The construct with the tangent of data values. If the
            operation was in-place then `None` is returned.
    
    **Examples:**

    >>> f.Units
    <Units: degrees_north>
    >>> print(f.array)
    [[-45 0 45 --]]
    >>> f.tan(inplace=True)
    >>> f.Units
    <Units: 1>
    >>> print(f.array)
    [[-1.0 0.0 1.0 --]]
    
    >>> f.Units
    <Units: m s-1>
    >>> print(f.array)
    [[1 2 3 --]]
    >>> e = f.tan()
    >>> e.Units
    <Units: 1>
    >>> print(e.array)
    [[1.55740772465 -2.18503986326 -0.142546543074 --]]

        '''
        return self._apply_data_operation(
            'tan', bounds=bounds, inplace=inplace, i=i)


    def log(self, base=None, bounds=True, inplace=False, i=False):
        '''The logarithm of the data array.

    By default the natural logarithm is taken, but any base may be
    specified.
    
    .. seealso:: `exp`
    
    :Parameters:
    
        base: number, optional
            The base of the logiarthm. By default a natural logiarithm
            is taken.
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with the logarithm of data values. If the
            operation was in-place then `None` is returned.
    
    **Examples:**
    
    >>> f.data
    <CF Data(1, 2): [[1, 2]]>
    >>> f.log().data
    <CF Data: [[0.0, 0.69314718056]] ln(re 1)>
    
    >>> f.data
    <CF Data(1, 2): [[1, 2]] 2>
    >>> f.log().data
    <CF Data(1, 2): [[0.0, 0.69314718056]] ln(re 2 1)>
    
    >>> f.data
    <CF Data(1, 2): [[1, 2]] kg s-1 m-2>
    >>> f.log().data
    <CF Data(1, 2): [[0.0, 0.69314718056]] ln(re 1 m-2.kg.s-1)>
    
    >>> f.log(inplace=True)
    
    >>> f.Units
    <Units: >
    >>> f.log()
    ValueError: Can't take the logarithm to the base 2.718281828459045 of <Units: >

        '''
        return self._apply_data_operation(
            'log', bounds=bounds, inplace=inplace, i=i)


    def squeeze(self, axes=None, inplace=False, i=False):
        '''Remove size 1 dimensions from the data array

    .. seealso:: `insert_dimension`, `flip`, `transpose`
    
    :Parameters:
    
        axes: (sequence of) `int`, optional
            The size 1 axes to remove. By default, all size 1 axes are
            removed. Size 1 axes for removal are identified by their
            integer positions in the data array.
        
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with squeezed data. If the operation was
            in-place then `None` is returned.
    
    **Examples:**
    
    
    TODO
    
    >>> f.squeeze()
    
    >>> f.squeeze(1)
    
    >>> f.squeeze([2, -1])

        '''
        if i:
            _DEPRECATION_ERROR_KWARGS(self, 'squeeze', i=True) # pragma: no cover

        return super().squeeze(axes=axes, inplace=inplace)
    

    def trunc(self, bounds=True, inplace=False, i=False):
        '''Truncate the data, element-wise.

    The truncated value of the scalar ``x``, is the nearest integer
    ``i`` which is closer to zero than ``x`` is. I.e. the fractional
    part of the signed number ``x`` is discarded.
    
    .. versionadded:: 1.0
    
    .. seealso:: `ceil`, `floor`, `rint`
    
    :Parameters:
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with truncated data. If the operation was
            in-place then `None` is returned.
    
    **Examples:**
    
    >>> print(f.array)
    [-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
    >>> print(f.trunc().array)
    [-1. -1. -1. -1.  0.  1.  1.  1.  1.]
    >>> f.trunc(inplace=True)
    >>> print(f.array)
    [-1. -1. -1. -1.  0.  1.  1.  1.  1.]

        '''
        return self._apply_data_operation(
            'trunc', bounds=bounds, inplace=inplace, i=i)

    
    def identities(self):
        '''Return all possible identities.

    The identities comprise:
    
    * The "standard_name" property.
    * The "id" attribute, preceeded by ``'id%'``.
    * The "cf_role" property, preceeded by ``'cf_role='``.
    * The "axis" property, preceeded by ``'axis='``.
    * The "long_name" property, preceeded by ``'long_name='``.
    * All other properties (including "standard_name"), preceeded by
      the property name and an ``'='``.
    * The coordinate type (``'X'``, ``'Y'``, ``'Z'`` or ``'T'``).
    * The netCDF variable name, preceeded by ``'ncvar%'``.
    
    The identities of the bounds, if present, are included (with the
    exception of the bounds netCDF variable name).

    .. versionadded:: 3.0.0
    
    .. seealso:: `id`, `identity`
    
    :Returns:
    
        `list`
            The identities.
    
    **Examples:**
    
    >>> f.properties()
    {'foo': 'bar',
     'long_name': 'Air Temperature',
     'standard_name': 'air_temperature'}
    >>> f.nc_get_variable()
    'tas'
    >>> f.identities()
    ['air_temperature',
     'long_name=Air Temperature',
     'foo=bar',
     'standard_name=air_temperature',
     'ncvar%tas']
    
    >>> f.properties()
    {}
    >>> f.bounds.properties()
    {'axis': 'Z',
     'units': 'm'}
    >>> f.identities()
    ['axis=Z', 'units=m', 'ncvar%z']

        '''
        identities = super().identities()
        
        bounds = self.get_bounds(None)
        if bounds is not None:
            identities.extend([i for i in bounds.identities()
                               if i not in identities])
# TODO ncvar AND?

        return identities


    def identity(self, default='', strict=False, relaxed=False,
                 nc_only=False, relaxed_identity=None):
        '''Return the canonical identity.

    By default the identity is the first found of the following:
    
    * The "standard_name" property.
    * The "id" attribute, preceeded by ``'id%'``.
    * The "cf_role" property, preceeded by ``'cf_role='``.
    * The "axis" property, preceeded by ``'axis='``.
    * The "long_name" property, preceeded by ``'long_name='``.
    * The netCDF variable name, preceeded by ``'ncvar%'``.
    * The coordinate type (``'X'``, ``'Y'``, ``'Z'`` or ``'T'``).
    * The value of the *default* parameter.

    If no identity can be found on the construct then the identity is
    taken from the bounds, if present (with the exception of the
    bounds netCDF variable name).
    
    .. seealso:: `id`, `identities`
    
    :Parameters:
    
        default: optional
            If no identity can be found then return the value of the
            default parameter.
    
        strict: `bool`, optional 
            If True then the identity is the first found of only the
            "standard_name" property or the "id" attribute.

        relaxed: `bool`, optional
            If True then the identity is the first found of only the
            "standard_name" property, the "id" attribute, the
            "long_name" property or the netCDF variable name.

        nc_only: `bool`, optional       
            If True then only take the identity from the netCDF
            variable name.

    :Returns:
    
            The identity.
    
    **Examples:**
    
    >>> f.properties()
    {'foo': 'bar',
     'long_name': 'Air Temperature',
     'standard_name': 'air_temperature'}
    >>> f.nc_get_variable()
    'tas'
    >>> f.identity()
    'air_temperature'
    >>> f.del_property('standard_name')
    'air_temperature'
    >>> f.identity(default='no identity')
    'air_temperature'
    >>> f.identity()
    'long_name=Air Temperature'
    >>> f.del_property('long_name')
    >>> f.identity()
    'ncvar%tas'
    >>> f.nc_del_variable()
    'tas'
    >>> f.identity()
    'ncvar%tas'
    >>> f.identity()
    ''
    >>> f.identity(default='no identity')
    'no identity'
    
    >>> f.properties()
    {}
    >>> f.bounds.properties()
    {'axis': 'Z',
     'units': 'm'}
    >>> f.identity()
    'axis=Z'

        '''
        if relaxed_identity:
            _DEPRECATAION_ERROR_KWARGS(
                self, 'identity', relaxed_identity=True) # pragma: no cover
            
        identity = super().identity(default=None, strict=strict,
                                    relaxed=relaxed, nc_only=nc_only)

        if identity is not None:
            return identity

        bounds = self.get_bounds(None)
        if bounds is not None:
            out = bounds.identity(default=None, strict=strict,
                                  relaxed=relaxed, nc_only=nc_only)

            if out is not None and not out.startswith('ncvar%'):
                return out
        #--- End: if
                
        return default


    def inspect(self):
        '''Inspect the object for debugging.

    .. seealso:: `cf.inspect`

    :Returns: 

        `None`

        '''
        print(cf_inspect(self)) # pragma: no cover


    def rint(self, bounds=True, inplace=False, i=False):
        '''Round the data to the nearest integer, element-wise.

    .. versionadded:: 1.0
    
    .. seealso:: `ceil`, `floor`, `trunc`
    
    :Parameters:
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
            
            The construct with rounded data. If the operation was
            in-place then `None` is returned.
    
    **Examples:**
    
    >>> print(f.array)
    [-1.9 -1.5 -1.1 -1.   0.   1.   1.1  1.5  1.9]
    >>> print(f.rint().array)
    [-2. -2. -1. -1.  0.  1.  1.  2.  2.]
    >>> f.rint(inplace=True)
    >>> print(f.array)
    [-2. -2. -1. -1.  0.  1.  1.  2.  2.]

        '''
        return self._apply_data_operation(
            'rint', bounds=bounds, inplace=inplace, i=i)


    def round(self, decimals=0, bounds=True, inplace=False, i=False):
        '''Round the data to the given number of decimals.

    Data elements are evenly rounded to the given number of decimals.
    
    .. note:: Values exactly halfway between rounded decimal values
              are rounded to the nearest even value. Thus 1.5 and 2.5
              round to 2.0, -0.5 and 0.5 round to 0.0, etc. Results
              may also be surprising due to the inexact representation
              of decimal fractions in the IEEE floating point standard
              and errors introduced when scaling by powers of ten.
     
    .. versionadded:: 1.1.4
    
    .. seealso:: `ceil`, `floor`, `rint`, `trunc`
    
    :Parameters:
    	
        decimals: `int`, optional
            Number of decimal places to round to (0 by default). If
            decimals is negative, it specifies the number of positions
            to the left of the decimal point.
    
        bounds: `bool`, optional
            If False then do not alter any bounds. By default any
            bounds are also altered.
    
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parameter instead.
    
    :Returns:
    
            The construct with rounded data. If the operation was
            in-place then `None` is returned.
    
    **Examples:**
    
    >>> print(f.array)
    [-1.81, -1.41, -1.01, -0.91,  0.09,  1.09,  1.19,  1.59,  1.99])
    >>> print(f.round().array)
    [-2., -1., -1., -1.,  0.,  1.,  1.,  2.,  2.]
    >>> print(f.round(1).array)
    [-1.8, -1.4, -1. , -0.9,  0.1,  1.1,  1.2,  1.6,  2. ]
    >>> print(f.round(-1).array)
    [-0., -0., -0., -0.,  0.,  0.,  0.,  0.,  0.]

        '''
        return self._apply_data_operation(
            'round', bounds=bounds, inplace=inplace, i=i,
            decimals=decimals)


    def roll(self, iaxis, shift, inplace=False, i=False):
        '''Roll the data along an axis.

    .. seealso:: `insert_dimension`, `flip`, `squeeze`, `transpose`
    
    :Parameters:
    
        iaxis: `int`
            TODO
            
        inplace: `bool`, optional
            If True then do the operation in-place and return `None`.
    
        i: deprecated at version 3.0.0
            Use *inplace* parmaeter instead.
    
    :Returns:
    
    TODO
    
    **Examples:**
    
    TODO

        '''
        return self._apply_data_operation(
            'roll', iaxis, shift, inplace=inplace, i=i)


    # ----------------------------------------------------------------
    # Deprecated attributes and methods
    # ----------------------------------------------------------------
    @property
    def hasbounds(self):
        '''Deprecated at version 3.0.0. Use method 'has_bounds' instead.
        
        '''
        _DEPRECATION_ERROR_ATTRIBUTE(
            self, 'hasbounds',
            "Use method 'has_bounds' instead.") # pragma: no cover

        
    def expand_dims(self, position=0, i=False):
        '''Insert a size 1 axis into the data array.

    Deprecated at version 3.0.0. Use method 'insert_dimension'
    instead.

        '''
        _DEPRECATION_ERROR_METHOD(
            self, 'expand_dims',
            "Use method 'insert_dimension' instead.") # pragma: no cover

        
#--- End: class
