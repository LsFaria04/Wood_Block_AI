from AppState import AppState
import pygame

def main():
    state = AppState()
    while state.state != 3:   
        state.step()

if __name__ == "__main__":
    main()