from AppState import AppState, STATE_EXIT

def main():
    '''
    Main function of the App. Includes the game loop.
    '''
    state = AppState()
    while state.state != STATE_EXIT:   
        state.step()

if __name__ == "__main__":
    main()