Plots
===

## Colors

```
c1 = "#5759aa"  # blue
c2 = "#9c4c36" # red
# https://meyerweb.com/eric/tools/color-blend/#9C4C36:000000:9:hex
c1k = "#3F417C" #"#47498B"  # blue 30% black
c2k = "#803E2C" #"#7D3D2B"  # red 30% black
c3 = "#800080"  # purple https://www.rapidtables.com/web/color/purple-color.html
c4 = "#9400D3"  # darkviolet
```



## Results

### Comparison to literature

- [x] compare to **experiments**
- [ ] how big are the errors we're seeing?
- [ ] compare to BTE results

### Overview results

- [ ] $\kappa$ vs. $\sigma^{\rm A}$ 
    - [ ] by spacegroup?
- [ ] histogram of thermal conductivities
- [ ] overview of non-trivial dynamical effects we see
    - [ ] (onset of) phase transitions
    - [ ] defect formation
    - [ ] dynamical stabilization

## Implementation

### Heat flux

- [ ] Heat flux (total)
- [ ] Heat flux autocorrelation (total)
- [ ] Heat flux (w/o gauge-invariant part)
- [ ] resulting autocorrelation function
- [ ] comparison resulting thermal conductivities

### Noise cancelling

- [ ] filtering strategy



## Problems

- [ ] how to assess supercell size error?
- [ ] how to assess finite-time error?
    - [ ] thermal conductivity as function of simulation time
        - [ ] LJ
        - [ ] materials w/ 60ps simulation time