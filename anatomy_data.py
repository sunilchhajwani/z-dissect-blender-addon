"""Anatomy data structures for Z-Dissect - integrated with Z-Anatomy."""

import bpy

# Z-Anatomy collection names (from Startup.blend)
# Collections use a dot prefix for ordering
ZANATOMY_COLLECTIONS = [
    '.Skeletal system',
    '.Muscular insertions',
    '.Joints',
    '.Muscular system',
    '.Cardiovascular system',
    '.Lymphoid organs',
    '.Nervous system & Sense organs',
    '.Visceral systems',
    '.Regions of human body',
    '.Reference lines, planes & movements',
]

# Mapping from Z-Anatomy collections to Z-Dissect systems
COLLECTION_TO_SYSTEM = {
    '.Muscular system': 'Muscular System',
    '.Skeletal system': 'Skeletal System',
    '.Nervous system & Sense organs': 'Nervous System',
    '.Cardiovascular system': 'Cardiovascular System',
    '.Visceral systems': 'Visceral Systems',
    '.Joints': 'Skeletal System',
    '.Muscular insertions': 'Muscular System',
    '.Lymphoid organs': 'Lymphoid System',
}

# System display names
SYSTEM_NAMES = {
    'Muscular System': 'Muscular System',
    'Skeletal System': 'Skeletal System',
    'Nervous System': 'Nervous System',
    'Cardiovascular System': 'Cardiovascular System',
    'Visceral Systems': 'Visceral Systems',
    'Lymphoid System': 'Lymphoid System',
    'Regions of human body': 'Body Regions',
}

# Region hierarchy (simplified TA2 structure)
# These map to collections and sub-collections in Z-Anatomy
REGIONS = {
    'Head & Neck': ['Head', 'Face', 'Neck', 'Skull', 'Mandible', 'Cervical'],
    'Thorax': ['Thorax', 'Chest', 'Ribs', 'Sternum', 'Diaphragm'],
    'Abdomen': ['Abdomen', 'Pelvis', 'Abdominal wall', 'Peritoneum'],
    'Upper Limb': ['Shoulder', 'Arm', 'Forearm', 'Hand', 'Clavicle', 'Scapula', 'Humerus', 'Radius', 'Ulna'],
    'Lower Limb': ['Hip', 'Thigh', 'Leg', 'Foot', 'Femur', 'Tibia', 'Fibula', 'Patella'],
    'Back': ['Back', 'Spine', 'Vertebral column', 'Sacrum'],
}

# Anatomy hierarchy: System -> Region -> [Parts]
# This is the primary data structure used by UI and selection operators
ANATOMY_HIERARCHY = {
    'Muscular System': {
        'Head & Neck': [
            'Masseter', 'Temporalis', 'Frontalis', 'Orbicularis oculi', 'Buccinator',
            'Orbicularis oris', 'Zygomaticus', 'Sternocleidomastoid', 'Trapezius',
            'Digastric', 'Mylohyoid', 'Geniohyoid', 'Platysma'
        ],
        'Upper Limb': [
            'Deltoid', 'Biceps brachii', 'Triceps brachii', 'Brachialis',
            'Brachioradialis', 'Pronator teres', 'Supinator', 'Flexor carpi radialis',
            'Flexor carpi ulnaris', 'Extensor carpi radialis', 'Extensor carpi ulnaris',
            'Thenar muscles', 'Hypothenar muscles'
        ],
        'Thorax': [
            'Pectoralis major', 'Pectoralis minor', 'Subclavius', 'Serratus anterior',
            'External intercostals', 'Internal intercostals', 'Diaphragm'
        ],
        'Abdomen': [
            'Rectus abdominis', 'External oblique', 'Internal oblique',
            'Transversus abdominis', 'Quadratus lumborum'
        ],
        'Lower Limb': [
            'Gluteus maximus', 'Gluteus medius', 'Gluteus minimus',
            'Tensor fasciae latae', 'Quadriceps femoris', 'Biceps femoris',
            'Semitendinosus', 'Semimembranosus', 'Adductor magnus',
            'Adductor longus', 'Gracilis', 'Sartorius', 'Gastrocnemius',
            'Soleus', 'Tibialis anterior', 'Tibialis posterior',
            'Peroneus longus', 'Peroneus brevis'
        ],
        'Back': [
            'Erector spinae', 'Iliocostalis', 'Longissimus', 'Spinalis',
            'Semispinalis', 'Multifidus', 'Rotatores'
        ]
    },
    'Skeletal System': {
        'Head & Neck': [
            'Skull', 'Mandible', 'Maxilla', 'Frontal bone', 'Parietal bone',
            'Temporal bone', 'Occipital bone', 'Sphenoid bone', 'Ethmoid bone',
            'Zygomatic bone', 'Nasal bone'
        ],
        'Thorax': [
            'Sternum', 'Ribs', 'Vertebral column (thoracic)', 'Clavicle', 'Scapula'
        ],
        'Abdomen': [
            'Vertebral column (lumbar)', 'Sacrum', 'Coccyx', 'Pelvis',
            'Ilium', 'Ischium', 'Pubis'
        ],
        'Upper Limb': [
            'Humerus', 'Radius', 'Ulna', 'Carpals', 'Metacarpals', 'Phalanges (hand)'
        ],
        'Lower Limb': [
            'Femur', 'Patella', 'Tibia', 'Fibula', 'Tarsals', 'Metatarsals', 'Phalanges (foot)'
        ],
        'Back': [
            'Vertebral column', 'Cervical vertebrae', 'Thoracic vertebrae',
            'Lumbar vertebrae', 'Sacrum', 'Coccyx'
        ]
    },
    'Nervous System': {
        'Central Nervous System': [
            'Brain', 'Cerebrum', 'Cerebellum', 'Brainstem', 'Spinal cord'
        ],
        'Peripheral Nervous System': [
            'Brachial plexus', 'Lumbosacral plexus',
            'Median nerve', 'Ulnar nerve', 'Radial nerve',
            'Femoral nerve', 'Sciatic nerve', 'Tibial nerve', 'Fibular nerve'
        ]
    },
    'Cardiovascular System': {
        'Heart': ['Heart', 'Atria', 'Ventricles'],
        'Arteries': ['Aorta', 'Carotid arteries', 'Subclavian arteries', 'Femoral arteries'],
        'Veins': ['Vena cava', 'Jugular veins', 'Femoral veins']
    },
    'Visceral Systems': {
        'Respiratory': ['Lungs', 'Trachea', 'Bronchi'],
        'Digestive': ['Stomach', 'Intestines', 'Liver', 'Pancreas'],
        'Urinary': ['Kidneys', 'Ureters', 'Bladder'],
        'Reproductive': ['Reproductive organs']
    }
}

# Common Latin/English name mappings for muscles
MUSCLE_NAME_MAP = {
    # Latin -> English (Z-Anatomy uses Latin names)
    'Musculus biceps brachii': 'Biceps brachii',
    'Musculus triceps brachii': 'Triceps brachii',
    'Musculus deltoideus': 'Deltoid',
    'Musculus pectoralis major': 'Pectoralis major',
    'Musculus pectoralis minor': 'Pectoralis minor',
    'Musculus latissimus dorsi': 'Latissimus dorsi',
    'Musculus trapezius': 'Trapezius',
    'Musculus sternocleidomastoideus': 'Sternocleidomastoid',
    'Musculus masseter': 'Masseter',
    'Musculus temporalis': 'Temporalis',
    'Musculus orbicularis oculi': 'Orbicularis oculi',
    'Musculus orbicularis oris': 'Orbicularis oris',
    'Musculus buccinator': 'Buccinator',
    'Musculus zygomaticus': 'Zygomaticus',
    'Musculus frontalis': 'Frontalis',
    'Musculus platysma': 'Platysma',
    'Musculus digastricus': 'Digastric',
    'Musculus mylohyoideus': 'Mylohyoid',
    'Musculus geniohyoideus': 'Geniohyoid',
    'Musculus rectus abdominis': 'Rectus abdominis',
    'Musculus obliquus externus abdominis': 'External oblique',
    'Musculus obliquus internus abdominis': 'Internal oblique',
    'Musculus transversus abdominis': 'Transversus abdominis',
    'Musculus quadratus lumborum': 'Quadratus lumborum',
    'Musculus gluteus maximus': 'Gluteus maximus',
    'Musculus gluteus medius': 'Gluteus medius',
    'Musculus gluteus minimus': 'Gluteus minimus',
    'Musculus tensor fasciae latae': 'Tensor fasciae latae',
    'Musculus quadriceps femoris': 'Quadriceps femoris',
    'Musculus biceps femoris': 'Biceps femoris',
    'Musculus semitendinosus': 'Semitendinosus',
    'Musculus semimembranosus': 'Semimembranosus',
    'Musculus adductor magnus': 'Adductor magnus',
    'Musculus adductor longus': 'Adductor longus',
    'Musculus gracilis': 'Gracilis',
    'Musculus sartorius': 'Sartorius',
    'Musculus gastrocnemius': 'Gastrocnemius',
    'Musculus soleus': 'Soleus',
    'Musculus tibialis anterior': 'Tibialis anterior',
    'Musculus tibialis posterior': 'Tibialis posterior',
    'Musculus peroneus longus': 'Peroneus longus',
    'Musculus peroneus brevis': 'Peroneus brevis',
    'Musculus erector spinae': 'Erector spinae',
    'Musculus iliocostalis': 'Iliocostalis',
    'Musculus longissimus': 'Longissimus',
    'Musculus spinalis': 'Spinalis',
    'Musculus semispinalis': 'Semispinalis',
    'Musculus multifidus': 'Multifidus',
    'Musculus rotatores': 'Rotatores',
    'Musculus intercostales externi': 'External intercostals',
    'Musculus intercostales interni': 'Internal intercostals',
    'Musculus diaphragma': 'Diaphragm',
    'Musculus brachialis': 'Brachialis',
    'Musculus brachioradialis': 'Brachioradialis',
    'Musculus pronator teres': 'Pronator teres',
    'Musculus supinator': 'Supinator',
    'Musculus flexor carpi radialis': 'Flexor carpi radialis',
    'Musculus flexor carpi ulnaris': 'Flexor carpi ulnaris',
    'Musculus extensor carpi radialis': 'Extensor carpi radialis',
    'Musculus extensor carpi ulnaris': 'Extensor carpi ulnaris',
}

# Common bone name mappings
BONE_NAME_MAP = {
    'Os frontale': 'Frontal bone',
    'Os parietale': 'Parietal bone',
    'Os temporale': 'Temporal bone',
    'Os occipitale': 'Occipital bone',
    'Os sphenoidale': 'Sphenoid bone',
    'Os ethmoidale': 'Ethmoid bone',
    'Mandibula': 'Mandible',
    'Maxilla': 'Maxilla',
    'Os zygomaticum': 'Zygomatic bone',
    'Os nasale': 'Nasal bone',
    'Vertebrae cervicales': 'Cervical vertebrae',
    'Vertebrae thoracicae': 'Thoracic vertebrae',
    'Vertebrae lumbales': 'Lumbar vertebrae',
    'Os sacrum': 'Sacrum',
    'Os coccygis': 'Coccyx',
    'Sternum': 'Sternum',
    'Costae': 'Ribs',
    'Clavicula': 'Clavicle',
    'Scapula': 'Scapula',
    'Humerus': 'Humerus',
    'Radius': 'Radius',
    'Ulna': 'Ulna',
    'Ossa carpi': 'Carpals',
    'Ossa metacarpi': 'Metacarpals',
    'Phalanges manus': 'Phalanges (hand)',
    'Os ilium': 'Ilium',
    'Os ischii': 'Ischium',
    'Os pubis': 'Pubis',
    'Femur': 'Femur',
    'Patella': 'Patella',
    'Tibia': 'Tibia',
    'Fibula': 'Fibula',
    'Ossa tarsi': 'Tarsals',
    'Ossa metatarsi': 'Metatarsals',
    'Phalanges pedis': 'Phalanges (foot)',
}

# Nerve name mappings
NERVE_NAME_MAP = {
    'Nervus medianus': 'Median nerve',
    'Nervus ulnaris': 'Ulnar nerve',
    'Nervus radialis': 'Radial nerve',
    'Nervus femoralis': 'Femoral nerve',
    'Nervus ischiadicus': 'Sciatic nerve',
    'Nervus tibialis': 'Tibial nerve',
    'Nervus fibularis': 'Fibular nerve',
    'Plexus brachialis': 'Brachial plexus',
    'Plexus lumbosacralis': 'Lumbosacral plexus',
    'Medulla spinalis': 'Spinal cord',
    'Encephalon': 'Brain',
    'Cerebrum': 'Cerebrum',
    'Cerebellum': 'Cerebellum',
    'Truncus encephali': 'Brainstem',
}

# Object name to system mapping (heuristic-based for Z-Anatomy naming)
OBJECT_SYSTEM_MAP = {}

# Object name to region mapping (heuristic)
OBJECT_REGION_MAP = {}

# Detected objects from blend file
DETECTED_OBJECTS = {
    'Muscular System': [],
    'Skeletal System': [],
    'Nervous System': [],
    'Cardiovascular System': [],
    'Other': []
}


def _detect_system_from_name(obj_name):
    """Detect anatomy system from object name using Z-Anatomy conventions."""
    name_lower = obj_name.lower()

    # Remove suffixes (.t, .j, .g, .st) for matching
    clean_name = obj_name.split('.')[0].lower()

    # Muscular markers (Latin and English)
    muscular_markers = [
        'musculus', 'muscle', 'musc', 'biceps', 'triceps', 'deltoid',
        'pectoral', 'abdominis', 'quadriceps', 'gastrocnemius', 'gluteus',
        'trapezius', 'latissimus', 'serratus', 'rhomboid', 'levator',
        'scalene', 'sternocleidomastoid', 'orbicularis', 'zygomatic',
        'buccinator', 'masseter', 'temporalis', 'frontalis', 'digastric',
        'mylohyoid', 'geniohyoid', 'platysma', 'brachialis', 'brachioradialis',
        'pronator', 'supinator', 'flexor', 'extensor', 'thenar', 'hypothenar',
        'adductor', 'gracilis', 'sartorius', 'soleus', 'tibialis', 'peroneus',
        'erector', 'iliocostalis', 'longissimus', 'spinalis', 'semispinalis',
        'multifidus', 'rotatores', 'intercostal', 'diaphragm', 'oblique'
    ]

    # Skeletal markers
    skeletal_markers = [
        'os ', 'bone', 'skeletal', 'femur', 'tibia', 'fibula',
        'humerus', 'radius', 'ulna', 'clavicle', 'scapula', 'pelvis',
        'sacrum', 'coccyx', 'sternum', 'rib', 'vertebra', 'cranium',
        'skull', 'mandible', 'maxilla', 'patella', 'carpal', 'metacarpal',
        'tarsal', 'metatarsal', 'phalanx', 'phalang', 'frontale', 'parietale',
        'temporale', 'occipitale', 'sphenoidale', 'ethmoidale', 'zygomaticum',
        'nasale', 'ilium', 'ischii', 'pubis'
    ]

    # Nervous markers
    nervous_markers = [
        'nerv', 'nerve', 'brain', 'spinal', 'ganglion', 'plexus',
        'cerebrum', 'cerebellum', 'brainstem', 'medulla', 'pons',
        'medianus', 'ulnaris', 'radialis', 'femoralis', 'ischiadicus',
        'tibialis', 'fibularis', 'encephalon'
    ]

    # Cardiovascular markers
    cardiovascular_markers = [
        'arter', 'artery', 'ven', 'vein', 'aorta', 'cardiac', 'heart',
        'coronary', 'pulmonary', 'vena', 'cava', 'capillar'
    ]

    # Check markers
    if any(m in clean_name for m in muscular_markers):
        return 'Muscular System'
    elif any(m in clean_name for m in skeletal_markers):
        return 'Skeletal System'
    elif any(m in clean_name for m in nervous_markers):
        return 'Nervous System'
    elif any(m in clean_name for m in cardiovascular_markers):
        return 'Cardiovascular System'

    return 'Other'


def _detect_region_from_name(obj_name):
    """Detect body region from object name."""
    name_lower = obj_name.lower()

    region_markers = {
        'Head & Neck': ['head', 'cranial', 'facial', 'neck', 'cervical', 'mandib', 'maxill',
                        'frontal', 'parietal', 'temporal', 'occipital', 'zygomatic', 'nasal',
                        'masseter', 'temporalis', 'sternocleidomastoid', 'platysma'],
        'Thorax': ['thorax', 'thoracic', 'chest', 'rib', 'sternum', 'pectoral',
                   'intercostal', 'diaphragm'],
        'Abdomen': ['abdomen', 'abdominal', 'pelvis', 'pelvic', 'rectus abdomin',
                    'oblique', 'transversus', 'quadratus'],
        'Upper Limb': ['shoulder', 'arm', 'forearm', 'hand', 'brachial', 'biceps', 'triceps',
                       'deltoid', 'clavicle', 'scapula', 'humerus', 'radius', 'ulna',
                       'carpal', 'metacarpal', 'phalang'],
        'Lower Limb': ['hip', 'thigh', 'leg', 'foot', 'femoral', 'gluteus', 'quadriceps',
                       'hamstring', 'tibia', 'fibula', 'patella', 'gastrocnemius', 'soleus',
                       'tarsal', 'metatarsal'],
        'Back': ['back', 'spine', 'vertebr', 'sacrum', 'erector', 'spinalis', 'longissimus',
                 'iliocostalis', 'multifidus']
    }

    for region, markers in region_markers.items():
        if any(m in name_lower for m in markers):
            return region

    return 'Unknown'


def _build_system_maps():
    """Build maps from Z-Anatomy objects to anatomy systems."""
    global OBJECT_SYSTEM_MAP, OBJECT_REGION_MAP, DETECTED_OBJECTS

    # Reset detected objects
    for key in DETECTED_OBJECTS:
        DETECTED_OBJECTS[key] = []

    # Safety check: bpy.data may be restricted during registration
    try:
        collections = bpy.data.collections
        objects = bpy.data.objects
    except AttributeError:
        # bpy.data not available yet (background mode or startup)
        return

    # First, check Z-Anatomy collections
    for collection in collections:
        col_name = collection.name

        # Map collection to system
        if col_name in COLLECTION_TO_SYSTEM:
            system = COLLECTION_TO_SYSTEM[col_name]
            for obj in collection.all_objects:
                if obj.type == 'MESH':
                    # Skip label objects
                    if any(suffix in obj.name for suffix in ['.t', '.j', '.g', '.st']):
                        continue
                    OBJECT_SYSTEM_MAP[obj.name] = system
                    DETECTED_OBJECTS[system].append(obj.name)

    # Then, for objects not in known collections, use heuristic detection
    for obj in objects:
        if obj.type == 'MESH' and obj.name not in OBJECT_SYSTEM_MAP:
            # Skip label objects
            if any(suffix in obj.name for suffix in ['.t', '.j', '.g', '.st']):
                continue

            system = _detect_system_from_name(obj.name)
            OBJECT_SYSTEM_MAP[obj.name] = system
            DETECTED_OBJECTS[system].append(obj.name)

            region = _detect_region_from_name(obj.name)
            OBJECT_REGION_MAP[obj.name] = region


def load_anatomy_data():
    """Load anatomy data from Z-Anatomy blend file."""
    _build_system_maps()

    # Print summary
    print("\n=== Z-Dissect Anatomy Data Loaded ===")
    for system, objects in DETECTED_OBJECTS.items():
        if objects:
            print(f"  {system}: {len(objects)} objects")
    print("=" * 40)


def get_object_system(obj_name):
    """Return the system for a given object."""
    return OBJECT_SYSTEM_MAP.get(obj_name, None)


def get_object_region(obj_name):
    """Return the region for a given object."""
    return OBJECT_REGION_MAP.get(obj_name, 'Unknown')


def get_system_regions(system_name):
    """Return regions for a given system."""
    # Return regions that have objects in this system
    regions_with_objects = set()

    for obj_name, obj_system in OBJECT_SYSTEM_MAP.items():
        if obj_system == system_name:
            region = OBJECT_REGION_MAP.get(obj_name, 'Unknown')
            if region != 'Unknown':
                regions_with_objects.add(region)

    return sorted(list(regions_with_objects)) if regions_with_objects else list(REGIONS.keys())


def get_region_parts(system_name, region_name):
    """Return parts for a given system and region."""
    parts = []

    for obj_name, obj_system in OBJECT_SYSTEM_MAP.items():
        if obj_system == system_name:
            obj_region = OBJECT_REGION_MAP.get(obj_name, 'Unknown')
            if obj_region == region_name:
                # Clean up name - remove suffixes and use English name
                clean_name = obj_name.split('.')[0]
                if clean_name in MUSCLE_NAME_MAP:
                    clean_name = MUSCLE_NAME_MAP[clean_name]
                elif clean_name in BONE_NAME_MAP:
                    clean_name = BONE_NAME_MAP[clean_name]
                elif clean_name in NERVE_NAME_MAP:
                    clean_name = NERVE_NAME_MAP[clean_name]
                parts.append(clean_name)

    return sorted(set(parts))


def get_all_systems():
    """Return all available anatomy systems."""
    systems = [s for s in SYSTEM_NAMES.keys()]
    # Add detected systems
    for system in DETECTED_OBJECTS.keys():
        if DETECTED_OBJECTS[system] and system not in systems:
            systems.append(system)
    return systems


def get_collection_for_system(system_name):
    """Return the Z-Anatomy collection name for a system."""
    for col_name, sys_name in COLLECTION_TO_SYSTEM.items():
        if sys_name == system_name:
            return col_name
    return None


def get_objects_in_system(system_name):
    """Return all mesh objects in a system."""
    collection_name = get_collection_for_system(system_name)
    if collection_name and collection_name in bpy.data.collections:
        collection = bpy.data.collections[collection_name]
        return [obj for obj in collection.all_objects
                if obj.type == 'MESH' and not any(suffix in obj.name for suffix in ['.t', '.j', '.g', '.st'])]
    return DETECTED_OBJECTS.get(system_name, [])


def get_muscle_objects():
    """Return all muscle objects in the scene."""
    return get_objects_in_system('Muscular System')


def get_skeletal_objects():
    """Return all skeletal objects in the scene."""
    return get_objects_in_system('Skeletal System')


def get_nervous_objects():
    """Return all nervous system objects in the scene."""
    return get_objects_in_system('Nervous System')