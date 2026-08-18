TILE_SIZE=32
ENEMY_COUNT=1
ENEMY_TYPES={
    "melee1":{
        "height":48,
        "width":48,
        "speed":2,
        "damage":20,
        "health":100,
        "view_radius":350,
        "image":"assets/enemy1.png"
    },

    "range1":{
        "height":48,
        "width":48,
        "speed":1,
        "damage":30,
        "health":80,
        "view_radius":500,
        "image":"assets/range1.png",
        "projectile_image":"assets/enemyprojectile1.png"
    }
}

# ITEM_TYPES={
#     "mace":{
#         "damage":30,
#         "cooldown":45,#frames
#         "image":"assets/mace.png"
#     }
# }