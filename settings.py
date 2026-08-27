TILE_SIZE=32
ENEMY_COUNT=1
ENEMY_TYPES={
    "melee1":{
        "height":48,
        "width":48,
        "speed":1.5,
        "damage":20,
        "health":100,
        "view_radius":350,
        "image":"assets/melee1.png",
        "damaged_image":"assets/damaged_melee1.png",
        "xp_yield":25,
        "currency_yield":2
    },

    "range1":{
        "height":48,
        "width":48,
        "speed":1,
        "damage":32,
        "health":80,
        "view_radius":500,
        "image":"assets/range1.png",
        "damaged_image":"assets/damaged_range1.png",
        "projectile_image":"assets/enemyprojectile1.png",
        "xp_yield":100,
        "currency_yield":2
    }
}

SHOP_ITEMS={
    "items":{
            "SpellBook": 15,
            "Mace":18

        },
    "upgrades":{
        "Speed":3,
        "Damage":3,
        "Max Health":3,
        "Heal 25": 2,
        "Heal 50": 2,
        "Heal 100": 3,
        "Heal 200": 4,
    }
}

DIFFICULTY={
    "Easy":{
        "stats_multiplier":0.75,
        "speed_multiplier":0.9,
        "xp_multiplier":1.0
    },
    "Normal":{
        "stats_multiplier":1.0,
        "speed_multiplier":1.0,
        "xp_multiplier":1.0
    },
    "Hard":{
        "stats_multiplier":1.25,
        "speed_multiplier":1.1,
        "xp_multiplier":1.5
    },
    "Hardcore":{
        "stats_multiplier":1.5,
        "speed_multiplier":1.15,
        "xp_multiplier":2
    }

}

# ITEM_TYPES={
#     "mace":{
#         "damage":30,
#         "cooldown":45,#frames
#         "image":"assets/mace.png"
#     }
# }