First principles thermal transport in strongly anharmonic semiconductors and insulators
===

# Current Plan

## To Do's

- [x] Chapter 2: Lattice dynamics, phonons
    - [x] classical harmonic dynamics
    - [x] review
    - [x] -> Marcin/Chris
    - [ ] show phonon dispersions?
    - [ ] DOS?
    - [ ] idea: move Si and KCaF3 up, discuss there.
- [x] Chapter 3: heat transport
    - [x] Review Yair 
    - [x] -> Chris
- [ ] Chapter 4: Anharmoncity (short version of paper)
    - [ ] overview materials: 
        - [ ] sources (Springer, ICSD, MorelliSlack, …)
        - [ ] histogram sigmaA
- [ ] Chapter 5: Results
    - [ ] dedicated methods and benchmarks chapter?
    - [ ] compare experiment
    - [ ] Finite time effect estimation!
        - [ ] [biased/unbiased autocorr?](https://stats.stackexchange.com/a/343524/265607)
    - [ ] thermal conductivity for trustworthy materials
        - [ ] compare theory (?)
        - [ ] vs. sigma
    - [ ] Dynamical effects
- [ ] Outlook
    - [ ] Schnet
    - [ ] TDEP

# Initial Plan

## KW 15: analyze and plot

### 12.04.

- [x] submit remaining materials to LISE
- [x] integrate interpolation in GK workflow
    - [ ] ~~compute $\kappa^\alpha$ instead of $\kappa^{\alpha \beta}$~~
    - [x] add ha-q data to dataset
- [x] streamline and run for completed materials
- [ ] extract results and statistics
    - [ ] e.g. lifetimes
- [ ] submit el. DOS for CuI w/ and w/o defects

### 13.04.

- [x] update plots:
    - [x] thermal conductivity vs. experiment, w/ and w/o interpolation
    - [x] thermal conductivity vs. anharmonicity, w/ and w/o interpolation
- [x] List materials that are far away from exp.
- [x] List materials for which interpolation goes wrong
- [x] Choose materials for further analysis
    - [ ] CuI
    - [ ] KCaF3
    - [ ] AgI?
    - [ ] MgSb?
    - [ ] ?
- [ ] impact of simulation time? try to estimate

### 14.04.

- [x] discuss w/ Chris
    - [x] paper review

- [ ] benchmark chapter
    - [ ] MgO and CuI (for example)
    - [ ] heat flux
    - [ ] gauge invariant terms
    - [ ] harmonic flux (${\bf J}^{\rm ha-{\bf r}}$ and ${\bf J}^{\rm ha-{\bf q}}$)
    - [ ] with effective phonons?
    - [ ] noise filtering approach
    - [ ] analytic interpolation scheme
    - [ ] discuss convergence w.r.t. simulation time
    - [ ] lattice expansion? Comparison to NPT run?
- [x] schedule meeting w/ Matthias

### 15.04.

- [ ] prepare or start writing results

### 16.04.

- [ ] check time schedule

## KW 16: write

### 19.04.

- [ ] results: catch up with last week

- [x] paper review

### 20.04.

- [x] theory: DFT

### 21.04.

- [ ] theory: lattice dynamics

    - [ ] symmetry properties of dynamical matrix (Maradudin adaption)

- [x] theory: heat flux

- [ ] send out to reviewers

### 22.0

- [ ] results

### 23.04.

- [ ] implementation/benchmark

## KW 17: write and include feedback

### 26.04.

- [x] Treffen Matthias

- [ ] results

### 27.04.

- [ ] anharmonicity and screening

### 28.04.

- [ ] review comments

### 29.04.

- [ ] review comments

### 30.04.

- [ ] review comments and fine-tune
- [ ] send to Matthias

## Pre-Reviewers for thesis

### 1 | Many-body problem

- [x] Sebas

### 2 | Lattice dynamics

- [ ] Marcin

3 | Heat transport

- [x] Dr. Yair

### 4 | Implementation and benchmarking

- [ ] Marcel

### 5 | Anharmonicity

- [ ] Tom

### Results

- [ ] Chris

## Edits

- https://tex.stackexchange.com/a/47936/91226

## Style

- https://packages.oth-regensburg.de/ctan/macros/latex/contrib/sidenotes/caesar_example.pdf
- https://github.com/Pseudomanifold/latex-mimosis