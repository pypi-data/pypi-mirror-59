
=======
Gimbiseo
=======

gimbiseo HM-dialogue system (only support Chinese)


Code::
    from gimbiseo import *
    memory = ChineseMemory()
    d = Dialogue()
    with d.base:
        app = QApplication([])
        myWin=DialogueUI(d)
        myWin.show()
        app.exec_()


