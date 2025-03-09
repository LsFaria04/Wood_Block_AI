from AppState import AppState, STATE_EXIT

def main():
    state = AppState()
    while state.state != STATE_EXIT:   
        state.step()

if __name__ == "__main__":
    main()