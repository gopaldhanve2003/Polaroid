# Polaroid

A command-line tool to generate **print-authentic Polaroid-style images** using a data-driven film pipeline.

This project simulates **instant film characteristics** (color response, contrast, grain, optical softness) and renders images in a **Polaroid-style print layout**, optimized for **physical printing**.

---

## Features

* Apply **Polaroid-style film looks** (fresh, aged, vintage, cinematic, retro, B&W).
* Physically believable **instant-film grain and softness**.
* Process **single images or entire directories**.
* Generate **all effects** or **random selections**.
* Fully **JSON-driven effects** (no hard-coded values).
* Optional image compression for storage or sharing.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gopaldhanve2003/polaroid.git
   cd polaroid
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

> **Polaroid is always applied.**
> Effects modify the film look before the Polaroid layout is rendered.

---

### Single Image (default Polaroid)

```bash
python3 polaroid.py --input path/to/image.jpg
```

Applies the default **polaroid_classic** look and saves the output.

---

### Single Image with Effects

Apply one or more film effects:

```bash
python3 polaroid.py --input path/to/image.jpg --effects polaroid_classic_aged
```

Multiple effects generate multiple outputs:

```bash
python3 polaroid.py --input path/to/image.jpg --effects bw_classic vintage cinematic_kodak
```

---

### Generate All Effects

Generate one output per available effect:

```bash
python3 polaroid.py --input path/to/image.jpg --all
```

---

### Random Effects

Generate a random subset of effects:

```bash
python3 polaroid.py --input path/to/image.jpg --random 5
```

---

### Batch Processing

Process all images in a directory:

```bash
python3 polaroid.py --input-dir path/to/images
```

With specific effects:

```bash
python3 polaroid.py --input-dir path/to/images --effects polaroid_classic bw_soft
```

---

### List Available Effects

```bash
python3 polaroid.py --list-effects
```

---

### Compress Images

Compress images in a directory:

```bash
python3 polaroid.py --compress path/to/images --output path/to/compressed
```

With quality control (1–100):

```bash
python3 polaroid.py --compress path/to/images --output path/to/compressed --quality 80
```

---

## Effect Philosophy

* **`polaroid_classic`** → fresh instant print (baseline)
* **`polaroid_classic_aged`** → stored / yellowed print
* **B&W presets** → instant-film monochrome
* **Vintage / Retro / Cinematic** → stylistic film interpretations
* All effects are **print-first**, not Instagram-style filters

Effects are defined in `effects/*.json` and applied **before** the Polaroid layout.

---

## Contributing

Contributions are welcome, especially:

* New film looks (JSON only)
* Printer calibration presets
* Documentation improvements

Please keep effects **data-driven** and **print-authentic**.

---

Enjoy 🌤️📸
