from character import Character
import systems as sys

player_character = Character()

sys.luck_test(player_character)

sys.roll_dice(2)
sys.roll_dice(2)

player_character.add_gold(20)
player_character.add_item('Um bolo de Fezes')

