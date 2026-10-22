# Part VI — Communication Theory

Parts I–V built the tools to describe how circuits and systems shape signals: networks and transmission lines, transforms and transfer functions, sampling, the DFT and digital filters. Part VI turns those tools to the purpose for which much of electrical engineering exists — moving information from one place, or one time, to another. A communication link is a chain of signal-processing blocks between a source and a destination, with a channel in the middle that attenuates, distorts, delays and adds noise and interference, all within a power and bandwidth fixed by physics, batteries and regulators. This part asks how such a chain should be designed and how well it can possibly work, and answers in numbers: link budgets, signal-to-noise ratios, energy per bit, error probabilities and the Shannon capacity that bounds them.

By the end of this part you should understand:

- the generic model of a communication system and the roles of source, transmitter, channel, receiver and destination;
- how thermal and other noise, interference, bandwidth and signal-to-noise ratio set the performance of a link, and how to compute a link budget in decibels;
- how amplitude, frequency and phase modulation place an analog message on a carrier, what each costs in bandwidth and power, and how the superheterodyne receiver recovers it;
- how analog messages are digitised (PCM, delta modulation), how bits are put on a line (line coding) or a carrier (ASK, FSK, PSK, QPSK, QAM), and why the matched filter is the optimum receiver;
- how bit-error probability depends on $E_b/N_0$ for each modulation, and how the power–bandwidth trade-off is bounded by channel capacity;
- what entropy, mutual information and channel capacity mean, and how source and channel codes approach the theoretical limits;
- how random-process models describe communication noise, noise figure and detection performance;
- how radio propagation, fading and multipath shape wireless systems, and how cellular architecture, multiple access, OFDM and MIMO respond to them;
- how fibre attenuation and dispersion limit optical links, and how S-parameters and antennas describe the RF front end.

| Chapter | Central question | What it delivers |
|---|---|---|
| [25. Communication-System Fundamentals](25-communication-system-fundamentals.md) | What is a communication system made of, and which quantities decide how well it works? | System model, sources, transmitters and receivers, channel models, $kTB$ noise, bandwidth definitions, SNR and $E_b/N_0$, performance measures and the Shannon bound |
| [26. Analog Communication](26-analog-communication.md) | How is an analog message carried on a carrier, and what does each method cost and buy? | AM, DSB-SC, SSB, VSB, FM and PM; modulation indices and Bessel spectra; Carson's rule; modulators, demodulators and PLLs; the superheterodyne; noise figures of merit and threshold |
| [27. Digital Communication](27-digital-communication.md) | How are bits turned into waveforms, and how often does the receiver decide wrongly? | PCM and companding, delta modulation, line codes, Nyquist pulse shaping, constellations, ASK/FSK/PSK, QPSK, QAM, matched filtering, BER and SER in AWGN |
| [28. Information Theory and Coding](28-information-theory-and-coding.md) | How much information can a channel carry, and how do codes approach that limit? | Entropy, mutual information, channel capacity, source coding and compression, error detection, block and convolutional codes, modern coding methods |
| [29. Random Signals and Communication Noise](29-random-signals-and-communication-noise.md) | How is noise modelled as a random process, and how does it set detection performance? | Gaussian and white-noise models, noise bandwidth, noise figure and cascades, detection in noise, BER and SER, performance trade-offs |
| [30. Wireless and Mobile Communications](30-wireless-and-mobile-communications.md) | How do real radio paths behave, and how do mobile systems cope with them? | Path loss, fading, multipath, diversity, cellular architecture, multiple access, OFDM, MIMO, link budgets and system performance |
| [31. Optical Communications](31-optical-communications.md) | What limits transmission over optical fibre, and how are fibre links designed? | Fibre attenuation and dispersion, optical transmitters and receivers, WDM, optical link budgets and system limits |
| [32. RF and Microwave Fundamentals](32-rf-and-microwave-fundamentals.md) | How do circuits and antennas behave at radio and microwave frequencies? | RF signal behaviour, matching, S-parameters, RF components and resonators, microwave networks, antennas, radiation patterns, gain and directivity, RF measurements |

Part VI draws on almost everything before it. Fourier analysis and distortion (Chapter 18) describe channels; sampling and quantization (Chapters 19, 21) underlie PCM; the DFT (Chapter 22) is the engine of OFDM; digital and adaptive filters (Chapters 23–24) implement pulse shaping and equalisation; resonant circuits and transmission lines (Chapters 13–14) return as preselectors, matching networks and the Smith chart. Part VII reuses its feedback ideas: phase-locked loops and automatic gain control are control systems, analysed with the stability tools of Chapter 34. Probability and random processes are recapped, not derived (*The Mathematics Universe*); wave and antenna physics belong to *Engineering Physics*; the transistor circuits of amplifiers, mixers and converters to *Electronics & Computing*.
