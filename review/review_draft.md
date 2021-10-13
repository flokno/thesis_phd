Thesis Review
===

## Matthias

> Es gibt insbesondere 2 Dinge, die mir noch nicht gefallen:
>
> a) Beschreibung und kritische Diskussion der verschiedenen Näherungen und der damit verbundene Fehler. Das muss genauer und detaillierter dargestellt werden. Zu zero-point effects und zu isotopes gibt es eigentlich schon einige Ideen in der Literatur, wie man die abschätzend berücksichtigen kann. Das sollte auch diskutiert werden.
>
> b) Die Vergleiche mit BT müssen ausgebaut und genauer geführt werden. Die primäre Motivation der Arbeit war ja, festzustellen, wann BT nicht mir zuverlässig funktioniert. Und hier kannst/solltest du die BT Rechnungen aus der Literatur genauer diskutieren. Es gibt ja einige BT Beispiele, die für "sigma^A groesser als 0.4" Systeme durchgeführt wurden.

### a) Näherungen und Fehler

Zero-point effects / NQE:

- suggested in     [1]S. Volz *et al.*, Microelectron J **31**, 815 (2000).  

- Scrutinized in     [1]J. E. Turney, A. J. H. McGaughey, and C. H. Amon, Phys Rev B **79**, 224305 (2009).  

  → no systematic improvement bc different error cancellations

  → "The mapping of classical phonons onto an equivalent quantum system is approximately correct only at high temperatures, where QCs are unnecessary."

- also checked in     [1]M. Puligheddu *et al.*, Phys Rev Mater **3**, 085401 (2019).  with similar conclusion:

  "... we ﬁnd that using BE heat capacities with MD lifetimes (A2) worsens rather than  improves the agreement with the BTE-ALD results (A4). In agreement with Ref. [26], BE treatment of heat capacities together with MD lifetimes is ruled out as a possible quantum correction for classical MD simulations of thermal conductivity."

Isotopes:

- correction available from perturbation theory by treating mass disorder as pert. Hamiltonian

- correction formula due to Tang&Dong for MgO

  - use?

- no general correction scheme for aiGK besides explicit "alloying" in the supercell

  → could be tested w/ ML potential

### b) BT

- [x] überblick literatur
  - [x] welche Studien
  - [x] welche Art von BTE
- [x] überlapp mit unseren materialien, insbes bei >3rd order BTE
- [x]  trend 3rd vs. 4th order, vgl Xia/Ravichandran
- [x]  Diskussion von Kandidaten im Licht von sigma^A: NaCl und weitere

### DFT

- [ ] $T$, $T_s$: Clarify if there is more than notation
  - [ ] $T_s$: very definition of universal functional, see KohnSham1965, p.44f in Dreizler1990, in particular p. 48
  - [ ] v representability, uniqueness: p. 25 in Engel2011, p. 49 in Dreizler1990

### Lattice dynamics

- [ ] Shorten / move to appendix?

### Isotope effects

- [ ] use Eq. 1 from Tang to estimate effect, relate to other works
- [ ] suggest MA project on explicitly studying the effect based on a trained potential
  - [ ] Cite: Tang/Tamura, Haigis and dicussion therein, Garg?

### Embryos / Precursors

- [ ] ZrO2: Ferroelastic switch [Carbogno2014]
- [ ] Clathrates can host stable defects [Bhattacharya2017]
- [ ] Perovskites? -> Klarbring CMO [Klarbring.2018]
- [ ] Superionic conductors? -> Klarbring Ceria CeO2 [Klarbring.20183gv]
- [ ] precurs: new method how to find them.

### Style

- [ ] Gebrauch von "we"

### Chris

- BTE Diskussion:
  - schau nochmal insbes. NaCl an und diskutiere daran die BTE-Literatur im Vergleich zu aiGK
  - ggf weitere Beispiele?
  - nochmal betonen, dass die Frage mit den vorhandenen Daten (NOMAD!) beantwortet werden kann
  
- `Theory and methods` aufspalten in dedizierte Kapitel?

## Notation

- $\alpha, \beta, \gamma, \delta$: Cartesian components
- $\mu, \nu$: crystal-basis components
- $I, J$: atom labels
- $i, j$: atom labels in primitive cell
- ${\bf L}, {\bf K}$: lattice vectors ${\bf L} = L^\mu {\bf a}_\mu$ with lattice vectors ${\bf a}_\mu$

## 1 | Many Body Problem

- [x] Operatorhütchen?
- [x] Eq. (1.11) an den Anfang?
- [x] bessere Notation für $E^0_l$?
- [ ] peridioc systems: nötig? Vergleich mit Gitterdynamik
- [x] Zitation für Zitate
    - [ ] Peierls?
- [ ] $\mathcal V$ schon notwendig fuer $E^{\rm BO}$?

### Zitationen

- LDA:
    - 38, 169, 168 aus aims paper
    - 38: D. M. Ceperley and B. J. Alder. Ground state of the electron gas by a stochastic method. Phys. Rev. Lett., 45:566–569, 1980.
    - 169: J. P. Perdew and A. Zunger. Self-interaction correction to density-functional approximations for many-electron systems. Phys. Rev. B, 23:5048–5079, 1981.
    - 168: J. P. Perdew and Y. Wang. Accurate and simple analytic representation of the electron-gas correlation energy. Phys. Rev. B, 45:13244–13249, 1992.
- GGA:
    - 166, 26 and 27 in 167
    - 166: J. P. Perdew, K. Burke, and M. Ernzerhof. Generalized gradient approximation made simple. Phys. Rev. Lett., 77:3865–3868, 1997
    - 167: J. P. Perdew, J. A. Chevary, S. H. Vosko, K. A. Jackson, M. R. Pederson, D. J. Singh, and C. Fiolhais. Atoms, molecules, solids, and surfaces: Applications of the generalized gradient approximation for exchange and correlation. Phys. Rev. B, 46:6671–6687, 1992

## 2 | Lattice Dynamics

- [ ] L <-> M fuer Bravais-Vektoren?
- [x] erste Chp. 3, dann wird klarer was gebraucht wird
- [x] - [ ] Struktur?
    - [ ] HA
    - [ ] MD
    - [ ] HA@MD
- [x] Themen fuer Appendix markieren
- [x] `Lattice Dynamics` -> `Nuclear Dynamics`?
- [x] `Geometry optimization` -> appendix?
- [ ] Formel checken und anpassen
- [ ] Maradudin symmetries?
- [ ] group velocities?
- [ ] DOS?
- [x] ${\bf e_s} \to e^\alpha_s ~\text{oder}~ e_{s, \alpha}$?
- [ ] Notation aus Kapitel 1 anpassen in Bezug auf BvK/Periodizitaet.
- [x] intrinsic/extrinsic periodicity
- [ ] Brillouin zone, high-symmetry points?
- [ ] order:
  - [ ] extended systems/crystal, HA, MD, class. HA

## 3 | Heat Transport

- [x] clarify missing diffusion currents
- [ ] discuss limits of fourier equation, e.g., boundary terms
- [ ] definiere lebenszeit einmal allgemein
- [ ] rechne dann analytisch harmonisc/stoerungstheorie
- [ ] diskutiere dann fit an dynamik
- [ ] diskutiere scaling der lebenszeiten und interpolation
- [ ] vibes: speichere modenenergien statt besetzungen!

## 4 | Anharmonicity

- [ ] 