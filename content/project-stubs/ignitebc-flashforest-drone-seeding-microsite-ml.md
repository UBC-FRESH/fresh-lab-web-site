# FlashForest Drone Seeding Microsite Machine Learning

Status: Ongoing project

## Public Summary

Applied machine-learning work with FlashForest on classifying drone-imagery
microsites for aerial seeding and reforestation decision support.

The current workflow treats microsite selection as a four-class semantic
segmentation problem: background, good, fair, and poor. RGB orthomosaic tiles
are matched to pixel-wise segmentation masks prepared in Roboflow by forestry
experts, then used to train and evaluate U-Net models.

The project is less about claiming a finished production model and more about
building a reproducible baseline pipeline, diagnosing class imbalance, and
turning georeferenced prediction layers into operational planning inputs for
candidate planting points and drone mission planning.

## People And Roles

- Elaheh Ghasemi: machine-learning pipeline and technical report lead
- Kailey: TRANSFOR-M program student contributor
- Gregory Paradis: FRESH lead and supervisor

## Collaborators And Partners

- FlashForest
- Innovate BC / IgniteBC

## Outputs And Links

- ML4seeding public GitHub repository:
  https://github.com/UBC-FRESH/ML4seeding
- Reproducible U-Net semantic segmentation notebooks.
- Orthomosaic review, pseudo-orthomosaic construction, and image-tiling
  workflows.
- Evaluation workflow using accuracy, mean IoU, foreground mean IoU, and
  per-class IoU.
- Predicted segmentation-mask and georeferenced output workflow prototypes.
- Drone flight-path and operations-research post-processing prototypes.
- Private technical report retained as review material, not published on the
  site.

## Publications And References

Ghasemi, E. _Micro-site Classification from High Resolution Drone Images Using
Machine Learning_. Technical report, FRESH Lab review copy.

## Images And Assets

TBD.

## Source Notes

Maintained from:

- public repository `UBC-FRESH/ML4seeding`;
- private technical-report review PDF under `tmp/non-public-drafts/`.

Do not publish the private report PDF or any raw drone imagery, segmentation
masks, Roboflow exports, trained model binaries, or geospatial data unless
explicitly approved. Public-facing details that are safe to use:

- four microsite classes: background, good, fair, poor;
- 512 by 512 RGB tiles from high-resolution drone orthomosaics;
- Roboflow expert segmentation masks;
- spatial train/validation/test split to reduce spatial leakage;
- U-Net semantic segmentation baseline;
- early stopping, geometric augmentation, Dice loss, class weighting,
  low-information-tile filtering, and oversampling experiments;
- severe class imbalance as the main current modelling bottleneck;
- per-class IoU as an important evaluation metric;
- repo notebooks for orthomosaic review, pseudo-orthomosaic construction,
  tiling, U-Net training, predicted-mask stitching, drone flight paths, and
  operations-research post-processing.

## Open Questions

- What partner-approved language, images, and public deliverables can be listed?
- Should the final public page include preview images or diagrams from the
  public repository once a partner-approved asset set exists?
