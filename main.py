import sys
from game import Game

if __name__ == "__main__":
    use_agent = "--agent" in sys.argv or "-a" in sys.argv
    
    game = Game(use_agent=use_agent)
    
    if use_agent:
        print("Agent activé par défaut. Appuyez sur 'A' pour désactiver.")
    else:
        print("Mode manuel. Appuyez sur 'A' pour activer l'agent.")
    
    game.run()
