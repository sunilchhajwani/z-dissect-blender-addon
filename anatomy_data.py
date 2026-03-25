"""Anatomy data structures and TA2.csv parser for Z-Dissect."""

import csv
import os

# Anatomy hierarchy: system -> region -> parts
ANATOMY_HIERARCHY = {
    "Muscular System": {
        "Head & Neck": [
            "Masseter", "Temporalis", "Frontalis", "Orbicularis oculi", "Buccinator",
            "Orbicularis oris", "Zygomaticus", " Sternocleidomastoid", "Trapezius",
            "Digastric", "Mylohyoid", "Geniohyoid", "Platysma"
        ],
        "Upper Limb": [
            "Deltoid", "Biceps brachii", "Triceps brachii", "Brachialis",
            "Brachioradialis", "Pronator teres", "Supinator", "Flexor carpi radialis",
            "Flexor carpi ulnaris", "Extensor carpi radialis", "Extensor carpi ulnaris",
            "Thenar muscles", "Hypothenar muscles"
        ],
        "Thorax": [
            "Pectoralis major", "Pectoralis minor", "Subclavius", "Serratus anterior",
            "External intercostals", "Internal intercostals", "Diaphragm"
        ],
        "Abdomen": [
            "Rectus abdominis", "External oblique", "Internal oblique",
            "Transversus abdominis", "Quadratus lumborum"
        ],
        "Lower Limb": [
            "Gluteus maximus", "Gluteus medius", "Gluteus minimus",
            "Tensor fasciae latae", "Quadriceps femoris", "Biceps femoris",
            "Semitendinosus", "Semimembranosus", "Adductor magnus",
            "Adductor longus", "Gracilis", "Sartorius", "Gastrocnemius",
            "Soleus", "Tibialis anterior", "Tibialis posterior",
            "Peroneus longus", "Peroneus brevis"
        ],
        "Back": [
            "Erector spinae", "Iliocostalis", "Longissimus", "Spinalis",
            "Semispinalis", "Multifidus", "Rotatores"
        ]
    },
    "Skeletal System": {
        "Axial Skeleton": [
            "Skull", "Mandible", "Vertebral column", "Sacrum", "Coccyx",
            "Sternum", "Ribs"
        ],
        "Appendicular Skeleton": [
            "Clavicle", "Scapula", "Humerus", "Radius", "Ulna",
            "Carpals", "Metacarpals", "Phalanges (hand)",
            "Pelvis", "Femur", "Patella", "Tibia", "Fibula",
            "Tarsals", "Metatarsals", "Phalanges (foot)"
        ]
    },
    "Nervous System": {
        "Central Nervous System": [
            "Brain", "Cerebrum", "Cerebellum", "Brainstem", "Spinal cord"
        ],
        "Peripheral Nervous System": [
            "Brachial plexus", "Lumbosacral plexus",
            "Median nerve", "Ulnar nerve", "Radial nerve",
            "Femoral nerve", "Sciatic nerve", "Tibial nerve", "Fibular nerve"
        ]
    }
}

# TA2 term mappings (English -> TA2ID)
TA2_TERMS = {}

# Object name to system mapping (heuristic-based on Z-Anatomy naming)
OBJECT_SYSTEM_MAP = {}
OBJECT_REGION_MAP = {}


def _build_system_maps():
    """Build maps from object names to anatomy systems."""
    import bpy
    muscular_markers = ['musculus', 'muscle', 'musc', 'biceps', 'triceps', 'deltoid',
                        'pectoral', 'abdominis', 'quadriceps', 'gastrocnemius', 'gluteus',
                        'trapezius', 'latissimus', 'serratus', 'rhomboid', 'levator',
                        'scalene', 'sternocleidomastoid', 'orbicularis', 'zygomatic',
                        'buccinator', 'masseter', 'temporalis', 'frontalis', 'digastric',
                        'mylohyoid', 'geniohyoid', 'platysma', 'brachialis', 'brachioradialis',
                        'pronator', 'supinator', 'flexor', 'extensor', 'thenar', 'hypothenar',
                        'adductor', 'gracilis', 'sartorius', 'soleus', 'tibialis', 'peroneus',
                        'erector', 'iliocostalis', 'longissimus', 'spinalis', 'semispinalis',
                        'multifidus', 'rotatores', 'intercostal', 'diaphragm']

    skeletal_markers = ['os ', 'bone', 'skeletal', 'femur', 'tibia', 'fibula',
                         'humerus', 'radius', 'ulna', 'clavicle', 'scapula', 'pelvis',
                         'sacrum', 'coccyx', 'sternum', 'rib', 'vertebra', 'cranium',
                         'skull', 'mandible', 'patella', 'carpal', 'metacarpal', 'tarsal',
                         'metatarsal', 'phalang']

    nervous_markers = ['nerv', 'nerve', 'brain', 'spinal', 'ganglion', 'plexus',
                        'cerebrum', 'cerebellum', 'brainstem', 'medulla', 'pons']

    for obj in bpy.data.objects:
        name_lower = obj.name.lower()
        if obj.type == 'MESH':
            if any(m in name_lower for m in muscular_markers):
                OBJECT_SYSTEM_MAP[obj.name] = "Muscular System"
            elif any(m in name_lower for m in skeletal_markers):
                OBJECT_SYSTEM_MAP[obj.name] = "Skeletal System"
            elif any(m in name_lower for m in nervous_markers):
                OBJECT_SYSTEM_MAP[obj.name] = "Nervous System"


def load_anatomy_data():
    """Load TA2.csv and build anatomy maps."""
    _build_system_maps()


def get_object_system(obj_name):
    """Return the system for a given object."""
    return OBJECT_SYSTEM_MAP.get(obj_name, None)


def get_system_regions(system_name):
    """Return regions for a given system."""
    if system_name in ANATOMY_HIERARCHY:
        return list(ANATOMY_HIERARCHY[system_name].keys())
    return []


def get_region_parts(system_name, region_name):
    """Return parts for a given system and region."""
    if system_name in ANATOMY_HIERARCHY:
        regions = ANATOMY_HIERARCHY[system_name]
        if region_name in regions:
            return regions[region_name]
    return []


def get_all_systems():
    """Return all available anatomy systems."""
    return list(ANATOMY_HIERARCHY.keys())
