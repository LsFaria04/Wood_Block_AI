from GUI import GUI

def main():
    gui = GUI(1270, 720, "Wood Block")
    while True:   
        gui.drawRectangle(10,10,200, 200,(0,0,255))
        gui.refreshScreen()
        event = gui.getEvent()
        if(event == 'q'):
            break

    return 0

if __name__ == "__main__":
    main()