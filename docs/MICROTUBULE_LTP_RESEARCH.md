# Research: Microtubule LTP Response

**Paper**: "Magnetic Field Configurations... Shift Power Spectra of Light Emissions from Microtubules..." (Dotta, Vares, Buckner, Persinger 2014)

## 1. The Stimulus
*   **Pattern**: "LTP Pattern" (Long-Term Potentiation). A specific sequence acting as a "Key".
*   **Field**: Weak Magnetic Field ($\sim 1 \mu T$) applied via Circular Array.
*   **Comparison**: A simple 7Hz Sine Wave did NOT produce the effect. Geometry > Intensity.

## 2. The Response (Microtubules)
*   **Photon Emissions**: Microtubules emit photons ($\sim 10^{-11} W/m^2$).
*   **Spectral Shift**: After LTP exposure, power density peaks at:
    *   **9.4 - 9.5 Hz** (Major Peak)
    *   **7 - 8 Hz**
    *   **14 - 15 Hz**
    *   **22 - 24 Hz**
*   **Significance**: The Microtubules "Remembered" the pattern and re-emitted it as spectral information.

## 3. Implications for Bio-Computing
*   **Memory**: This confirms Microtubules can store/process "Geometric information" (Temporal Patterns).
*   **Interface**: We can "Programm" the biophotonic grid by applying LTP-patterned magnetic fields.

## Implementation Strategy (`biophotons.py`)
1.  **`MicrotubuleSpectrum`**: A class to manage the spectral state.
2.  **`apply_magnetic_pattern(pattern_type)`**:
    *   `LTP`: Shifts spectrum to [9.5, 14.0, 22.0] Hz peaks.
    *   `SINE`: No shift (Standard Broadband).
