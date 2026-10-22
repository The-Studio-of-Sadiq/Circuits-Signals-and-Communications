# Circuits, Signals and Communications — Master Syllabus

**Book 3 — Circuits, Signals & Communications Core**

**Objective:** Establish the theory of electrical networks, continuous- and discrete-time signals, system behaviour, information transmission and communication channels. This is the core that connects mathematical methods with almost every other EEE discipline.

Structure: 7 Parts · 35 Chapters. Each part is a folder `part-N-<slug>/`: its `README.md` is the part opener and `NN-<slug>.md` is Chapter NN.

The backbone is **circuit laws → network analysis → transients and AC → network theory → signals and systems → DSP → communication → control**. Every later part treats circuits and signals as the same mathematics seen from a different engineering destination.

---

## Part I — Circuit Fundamentals · `part-1-circuit-fundamentals/`

### Chapter 1. Electrical Quantities and Circuit Models · `01-electrical-quantities-and-circuit-models.md`
- Charge, current, voltage, and power
- Passive sign convention
- Energy
- Ideal and practical sources
- Independent and dependent sources
- Circuit elements
- Lumped-element assumptions
- Reference directions
- Circuit diagrams and notation
- Basic measurement concepts

### Chapter 2. Fundamental Circuit Laws · `02-fundamental-circuit-laws.md`
- Ohm's law
- Kirchhoff's Current Law
- Kirchhoff's Voltage Law
- Series and parallel combinations
- Voltage and current division
- Power balance
- Equivalent resistance
- Source transformations
- Network reduction
- Circuit topology

### Chapter 3. Network Analysis · `03-network-analysis.md`
- Nodal analysis
- Mesh analysis
- Supernodes and supermeshes
- Dependent-source circuits
- Network equations
- Matrix formulation
- Network topology
- Branch, node, and loop relationships
- Circuit solvability

### Chapter 4. Network Theorems · `04-network-theorems.md`
- Superposition
- Thévenin's theorem
- Norton's theorem
- Maximum power transfer
- Reciprocity
- Millman's theorem
- Source equivalence
- Equivalent networks
- Applications and limitations

### Chapter 5. Capacitors and Inductors · `05-capacitors-and-inductors.md`
- Capacitance
- Inductance
- Constitutive equations
- Energy storage
- Series and parallel combinations
- Initial conditions
- Mutual inductance
- Coupled coils
- Ideal versus practical components

## Part II — Transient and AC Analysis · `part-2-transient-and-ac-analysis/`

### Chapter 6. First-Order Circuits · `06-first-order-circuits.md`
- RC circuits
- RL circuits
- Natural response
- Forced response
- Time constants
- Switching behavior
- Initial and final values
- Piecewise excitation
- Step and impulse inputs

### Chapter 7. Second-Order Circuits · `07-second-order-circuits.md`
- RLC circuits
- Characteristic equations
- Overdamped response
- Underdamped response
- Critically damped response
- Natural frequency
- Damping ratio
- Resonance
- Transient energy exchange

### Chapter 8. Sinusoidal Steady-State Analysis · `08-sinusoidal-steady-state-analysis.md`
- Sinusoidal excitation
- RMS and average values
- Phasors
- Complex impedance
- Admittance
- AC nodal and mesh analysis
- Series and parallel AC circuits
- Resonance
- Frequency response
- Power calculations

### Chapter 9. AC Power · `09-ac-power.md`
- Instantaneous power
- Active and reactive power
- Apparent power
- Complex power
- Power factor
- Power-factor correction
- Energy consumption
- Non-sinusoidal considerations
- Practical power measurements

### Chapter 10. Three-Phase Circuits · `10-three-phase-circuits.md`
- Three-phase generation
- Phase sequence
- Star and delta connections
- Line and phase quantities
- Balanced loads
- Unbalanced loads
- Three-phase power
- Power measurement
- Neutral currents
- Practical applications

## Part III — Advanced Network Theory · `part-3-advanced-network-theory/`

### Chapter 11. Laplace-Domain Circuit Analysis · `11-laplace-domain-circuit-analysis.md`
- Circuit equations in the s-domain
- Impedance and admittance in the s-domain
- Initial conditions
- Transfer functions
- Pole-zero analysis
- Partial-fraction expansion
- Network response
- Transient and steady-state separation

### Chapter 12. Two-Port Networks · `12-two-port-networks.md`
- Z parameters
- Y parameters
- Hybrid parameters
- ABCD parameters
- Parameter conversion
- Cascaded networks
- Reciprocity and symmetry
- Applications in amplifiers and transmission systems

### Chapter 13. Network Frequency Response · `13-network-frequency-response.md`
- Magnitude and phase response
- Poles and zeros
- Bode plots
- Resonant circuits
- Quality factor
- Bandwidth
- Passive filters
- Active-filter interface
- Stability-related frequency behavior

### Chapter 14. Transmission Lines · `14-transmission-lines.md`
- Distributed parameters
- Telegrapher's equations
- Characteristic impedance
- Propagation constant
- Reflection coefficient
- Standing-wave ratio
- Impedance matching
- Smith chart
- Lossy and lossless lines
- High-frequency interconnects

## Part IV — Signals and Systems · `part-4-signals-and-systems/`

### Chapter 15. Signal Fundamentals · `15-signal-fundamentals.md`
- Continuous-time signals
- Discrete-time signals
- Periodic and aperiodic signals
- Even and odd signals
- Energy and power signals
- Unit step and impulse
- Ramp and exponential signals
- Time shifting and scaling
- Signal operations

### Chapter 16. System Fundamentals · `16-system-fundamentals.md`
- System classification
- Linearity
- Time invariance
- Causality
- Stability
- Memory and memoryless systems
- Continuous and discrete systems
- Input-output representations

### Chapter 17. Linear Time-Invariant Systems · `17-linear-time-invariant-systems.md`
- Impulse response
- Convolution
- Differential-equation representation
- Difference equations
- System response
- Eigenfunctions
- Causal and stable systems
- Interconnection of systems

### Chapter 18. Frequency-Domain System Analysis · `18-frequency-domain-system-analysis.md`
- Fourier-series representation
- Fourier transforms
- Frequency response
- Transfer functions
- Magnitude and phase
- Filtering
- Bandwidth
- Group delay
- Distortion
- Time-frequency relationships

### Chapter 19. Sampling and Reconstruction · `19-sampling-and-reconstruction.md`
- Sampling theorem
- Nyquist frequency
- Aliasing
- Ideal sampling
- Practical sampling
- Reconstruction
- Sample-and-hold behavior
- Quantization interface
- Anti-aliasing filters

### Chapter 20. Discrete-Time Signals and Systems · `20-discrete-time-signals-and-systems.md`
- Sequences
- Discrete-time convolution
- Difference equations
- Z-transform
- Discrete-time system functions
- Poles and zeros
- Discrete-time stability
- Digital filter fundamentals

## Part V — Digital Signal Processing · `part-5-digital-signal-processing/`

### Chapter 21. DSP Fundamentals · `21-dsp-fundamentals.md`
- Discrete-time representations
- Sampling and quantization
- Digital signal processing workflow
- Finite-precision effects
- Fixed-point and floating-point arithmetic
- Numerical error in DSP

### Chapter 22. Discrete Fourier Transform · `22-discrete-fourier-transform.md`
- DFT definition
- Inverse DFT
- Spectral interpretation
- FFT algorithms
- Spectral leakage
- Windowing
- Zero padding
- Spectral estimation

### Chapter 23. Digital Filters · `23-digital-filters.md`
- FIR filters
- IIR filters
- Difference-equation implementations
- Filter specifications
- Frequency transformations
- FIR design
- IIR design
- Stability
- Quantization effects
- Implementation constraints

### Chapter 24. Advanced Signal Processing · `24-advanced-signal-processing.md`
- Multirate processing
- Decimation and interpolation
- Adaptive filters
- Wiener filtering
- LMS algorithms
- Spectral estimation
- Time-frequency analysis
- Wavelet fundamentals
- Digital image and audio processing fundamentals

## Part VI — Communication Theory · `part-6-communication-theory/`

### Chapter 25. Communication-System Fundamentals · `25-communication-system-fundamentals.md`
- Communication-system models
- Information sources
- Transmitters and receivers
- Channels
- Noise and interference
- Bandwidth
- Signal-to-noise ratio
- Communication performance measures

### Chapter 26. Analog Communication · `26-analog-communication.md`
- Amplitude modulation
- Frequency modulation
- Phase modulation
- Modulation index
- Modulator and demodulator concepts
- Superheterodyne receivers
- Noise performance
- Analog communication systems

### Chapter 27. Digital Communication · `27-digital-communication.md`
- Pulse-code modulation
- Delta modulation
- Line coding
- ASK, FSK, and PSK
- QPSK
- QAM
- Constellation diagrams
- Symbol and bit rates
- Matched filtering
- Detection and error probability

### Chapter 28. Information Theory and Coding · `28-information-theory-and-coding.md`
- Information and entropy
- Mutual information
- Channel capacity
- Source coding
- Lossless compression
- Error detection
- Error-correcting codes
- Block codes
- Convolutional codes
- Fundamentals of modern coding methods

### Chapter 29. Random Signals and Communication Noise · `29-random-signals-and-communication-noise.md`
- Random processes in communication
- Gaussian noise
- White-noise models
- Noise bandwidth
- Noise figure
- Detection in noise
- BER and SER
- Performance trade-offs

### Chapter 30. Wireless and Mobile Communications · `30-wireless-and-mobile-communications.md`
- Radio propagation
- Path loss
- Fading
- Multipath
- Diversity
- Cellular architecture
- Multiple access
- OFDM fundamentals
- MIMO fundamentals
- Link budgets
- Wireless-system performance

### Chapter 31. Optical Communications · `31-optical-communications.md`
- Optical transmission fundamentals
- Fiber characteristics
- Attenuation
- Dispersion
- Optical transmitters
- Optical receivers
- Wavelength-division multiplexing
- Optical link budgets
- System limitations

### Chapter 32. RF and Microwave Fundamentals · `32-rf-and-microwave-fundamentals.md`
- RF signal behavior
- Impedance matching
- S-parameters
- RF components
- Resonators
- Microwave networks
- Antenna fundamentals
- Radiation patterns
- Gain and directivity
- RF measurements

## Part VII — Control-System Fundamentals · `part-7-control-system-fundamentals/`

### Chapter 33. Dynamic-System Modeling · `33-dynamic-system-modeling.md`
- Physical system models
- Differential equations
- Transfer functions
- Block diagrams
- Signal-flow graphs
- System interconnections
- Model simplification

### Chapter 34. Feedback and Stability · `34-feedback-and-stability.md`
- Open-loop and closed-loop systems
- Feedback principles
- Characteristic equations
- Stability concepts
- Routh–Hurwitz criterion
- Root-locus fundamentals
- Steady-state error
- Frequency-domain stability
- Bode and Nyquist methods

### Chapter 35. Control Design Fundamentals · `35-control-design-fundamentals.md`
- PID controllers
- Controller tuning
- Transient-response specifications
- Gain and phase margins
- State-space introduction
- Controllability
- Observability
- Digital control fundamentals

---

## Boundary

This book owns the mathematical theory of signals, communication, networks and introductory control. Transistor circuits, microcontrollers, motor hardware and practical robot controllers belong elsewhere.

## Relation to the other books

| Topic | Where it lives |
|---|---|
| Complex numbers, ODEs, Laplace/Fourier/Z transforms, probability and random processes (the mathematics itself) | The Mathematics Universe |
| Electromagnetic fields, Maxwell's equations, wave physics | Engineering Physics |
| Conductors, dielectrics, magnetic and optical-fibre materials | The Materials Core |
| Diodes, transistors, op-amp circuits, data converters, microcontrollers | Electronics & Computing |
| Generators, transformers, motors and power-system hardware | Electrical Energy & Machines |
| Practical robot controllers and embedded control hardware | Robotics and automation books |
| Networks, signals, systems, DSP, communication and introductory control theory | **This book** |
