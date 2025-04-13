# Memo AI

Memo AI is an agentic AI system developed in Python to restore, preserve, and enhance historical images. This project leverages state-of-the-art AI techniques to breathe new life into old or degraded photographs.

## 🚀 Features

- **Deblurring**: Removes motion blur and out-of-focus blur.
- **Super-Resolution**: Enhances resolution and clarity of low-quality images.
- **Image Inpainting**: Fills in missing or damaged parts of images.
- **Colorization**: Adds realistic colors to black-and-white images.
- **Noise Reduction**: Reduces noise and artifacts in scanned or compressed photos.
- **Face Enhancement**: Restores facial details in blurry or old portraits.

## 🧠 How Memo Helps with Image Restoration

AI models are used to:

- Remove blur caused by motion, poor lenses, or age-related degradation.
- Enhance resolution using super-resolution techniques.
- Fill in missing or torn parts of images through inpainting.
- Colorize black-and-white images while preserving realism and context.
- Reduce noise and artifacts for cleaner, sharper images.

## 🔐 Ethical & Contextual Considerations

When working with sensitive historical material, such as images from the Rwanda Genocide:

- **Preserve Authenticity**: Ensure accuracy and avoid AI hallucinations.
- **Maintain Original Copies**: Keep original images intact and clearly mark enhanced versions.
- **Human Validation**: Use human-in-the-loop validation for final archival usage to ensure ethical and accurate results.

## 🔁 High-Level Flow

```
    [ Image Upload or Metadata ]
                ↓
    ┌──────────────────────────────────
    │   🧠 OpenAI (Agentic Model)     |
    └──────────────────────────────────
                ↓
Decides: ["deblur", "upscale", "enhance_faces"]
                ↓
        Triggers Python Workers
┌──────────────┬────────────────────┬──────────────┐
│  FACEFIX     │  DEBLUR & ENHANCE  │   COLORIZE   │
└──────────────┴────────────────────┴──────────────┘
                ↓
    Combines Results + Logs + Metadata
                ↓
    [ Final Output + Report ]
```
