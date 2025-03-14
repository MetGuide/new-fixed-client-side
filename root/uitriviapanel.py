import ui
import dbg
import app
import net
import player
import chat
import app

class TriviaPanelWindow(ui.BoardWithTitleBar):

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)

	def BuildWindow(self):
		self.SetSize(244, 230)
		self.Show()
		self.AddFlag("float")
		self.AddFlag("movable")
		self.SetTitleName("GM: Panou event Trivia")
		self.SetCenterPosition()
		self.LoadWindow()

	def LoadWindow(self):
		self.textShow1 = ui.TextLine()
		self.textShow1.SetParent(self)
		self.textShow1.SetPosition(122, 50-17)
		self.textShow1.SetHorizontalAlignCenter()
		self.textShow1.SetDefaultFontName()
		self.textShow1.SetText("Întrebare (scrie în cãsuþã întrebarea)")
		self.textShow1.Show()

		self.ThinBoardList = ui.ThinBoardCircle()
		self.ThinBoardList.SetParent(self)
		self.ThinBoardList.SetSize(200, 25)
		self.ThinBoardList.SetPosition(22, 50)
		self.ThinBoardList.Show()

		self.statusInput = ui.EditLine()
		self.statusInput.SetParent(self.ThinBoardList)
		self.statusInput.SetSize(350, 18)
		self.statusInput.SetPosition(10, self.ThinBoardList.GetHeight()/2-5)
		self.statusInput.SetMax(64)
		self.statusInput.SetText("")
		self.statusInput.Show()

		self.textShow2 = ui.TextLine()
		self.textShow2.SetParent(self)
		self.textShow2.SetPosition(122, 100-17)
		self.textShow2.SetHorizontalAlignCenter()
		self.textShow2.SetDefaultFontName()
		self.textShow2.SetText("Rãspuns (scrie în cãsuþã rãspunsul)")
		self.textShow2.Show()

		self.ThinBoardList2 = ui.ThinBoardCircle()
		self.ThinBoardList2.SetParent(self)
		self.ThinBoardList2.SetSize(200, 25)
		self.ThinBoardList2.SetPosition(22, 100)
		self.ThinBoardList2.Show()

		self.statusInput2 = ui.EditLine()
		self.statusInput2.SetParent(self.ThinBoardList2)
		self.statusInput2.SetSize(350, 18)
		self.statusInput2.SetPosition(10, self.ThinBoardList2.GetHeight()/2-5)
		self.statusInput2.SetMax(64)
		self.statusInput2.SetText("")
		self.statusInput2.Show()

		self.ThinBoardList3 = ui.ThinBoardCircle()
		self.ThinBoardList3.SetParent(self)
		self.ThinBoardList3.SetSize(80, 25)
		self.ThinBoardList3.SetPosition(22, 150)
		self.ThinBoardList3.Show()

		self.textShow3 = ui.TextLine()
		self.textShow3.SetParent(self.ThinBoardList3)
		self.textShow3.SetPosition(40, -17)
		self.textShow3.SetHorizontalAlignCenter()
		self.textShow3.SetDefaultFontName()
		self.textShow3.SetText("Item (cod)")
		self.textShow3.Show()

		self.statusInput3 = ui.EditLine()
		self.statusInput3.SetParent(self.ThinBoardList3)
		self.statusInput3.SetSize(350, 18)
		self.statusInput3.SetPosition(10, self.ThinBoardList3.GetHeight()/2-5)
		self.statusInput3.SetMax(16)
		self.statusInput3.SetText("")
		self.statusInput3.Show()

		self.ThinBoardList4 = ui.ThinBoardCircle()
		self.ThinBoardList4.SetParent(self)
		self.ThinBoardList4.SetSize(80, 25)
		self.ThinBoardList4.SetPosition(22+80+40, 150)
		self.ThinBoardList4.Show()

		self.textShow4 = ui.TextLine()
		self.textShow4.SetParent(self.ThinBoardList4)
		self.textShow4.SetPosition(30, -17)
		self.textShow4.SetDefaultFontName()
		self.textShow4.SetText("Cât(e)?")
		self.textShow4.Show()

		self.statusInput4 = ui.EditLine()
		self.statusInput4.SetParent(self.ThinBoardList4)
		self.statusInput4.SetSize(350, 18)
		self.statusInput4.SetPosition(10, self.ThinBoardList4.GetHeight()/2-5)
		self.statusInput4.SetMax(16)
		self.statusInput4.SetText("")
		self.statusInput4.Show()

		self.btn1 = ui.Button()
		self.btn1.SetParent(self)
		self.btn1.SetPosition(32, 188)
		self.btn1.SetUpVisual("d:/ymir work/ui/public/xlarge_button_01.sub")
		self.btn1.SetOverVisual("d:/ymir work/ui/public/xlarge_button_02.sub")
		self.btn1.SetDownVisual("d:/ymir work/ui/public/xlarge_button_03.sub")
		self.btn1.SetText("Începe event Trivia")
		self.btn1.SetEvent(self.TriviaEvent)
		self.btn1.Show()

	def TriviaEvent(self):
		if len(self.statusInput.GetText()) == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Trebuie sã scrii prima datã o întrebare.")
			return

		if len(self.statusInput2.GetText()) == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Trebuie sã scrii prima datã un rãspuns.")
			return

		if len(self.statusInput3.GetText()) == 0 or len(self.statusInput4.GetText()) == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Trebuie sã introduci itemul ºi/sau cantitatea lui.")
			return

		net.SendChatPacket("/trivia xkzpwd31 \"" + str(self.statusInput.GetText()) + "\" \"" + str(self.statusInput2.GetText()) + "\" " + str(self.statusInput3.GetText()) + " " + str(self.statusInput4.GetText()))
		self.statusInput.SetText("")
		self.statusInput2.SetText("")
		self.statusInput3.SetText("")
		self.statusInput4.SetText("")
		self.Close()

	def OpenWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.BuildWindow()

	def Close(self):
		self.Hide()
