Yield Locus for Anisotropic Materials
====================================


`Yield Locus ` is a Python implementation of the Hill 1948 yield criteria for anisotropic plastic deformations. 
since its an extension to von mises theory, Lankford coefficient in rolling direction and transverse direction are taken into account.
No dependencies beside Python's standard library.


Installation
------------

```
pip install yieldlocus
```

Usage
-----
```
import yieldlocus
yield_locus.hill48(R0,R90,yield_stress)
```
Details
-----
For more information please refer
	1.	R. Hill. (1948). A theory of the yielding and plastic flow of anisotropic metals. Proc. Roy. Soc. London, 193:281–297
	2.	Study of Anisotropic Material Behavior for Inconel 625 Alloy 
		https://www.sciencedirect.com/science/article/pii/S2214785319322722

