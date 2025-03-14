import ui
import snd
import shop
import mouseModule
import player
import chr
import net
import uiCommon
import localeInfo
import chat
import item
import systemSetting #±èÁØÈ£
import player #±èÁØÈ£
# OFFLINE_SHOPS_METGUIDE
import constInfo
import app
import os
# END_OFFLINE_SHOPS_METGUIDE
# OFFLINE_SHOPS_METGUIDE
SHOP_VISIT=True
##### SHOP VISIT COLOR #####
SHOP_VISIT_COLOR=0xFFFFD700
g_privateShopAdvertisementBoardDict={}
# END_OFFLINE_SHOPS_METGUIDE
g_isBuildingPrivateShop = False
g_itemPriceDict={}
g_shopAdvertismentBoardSeen = {}

# OFFLINE_SHOPS_METGUIDE
def GetShopNamesRange():
	val=1.000
	try:
		with open("shop.cfg", 'r') as f:
			val=float(f.read().replace('\n', ''))
	except IOError:
		pass
	return float(val)
def SetShopNamesRange(pos):
	with open("shop.cfg", 'w+') as f:
		f.write(str(pos))
		f.close()
# END_OFFLINE_SHOPS_METGUIDE

def Clear():
	global g_itemPriceDict
	global g_isBuildingPrivateShop
	g_itemPriceDict={}
	g_isBuildingPrivateShop = False

	# @METGUIDEwork05 BEGIN
	global g_privateShopAdvertisementBoardDict
	g_privateShopAdvertisementBoardDict={}
	# @METGUIDEwork05 END

def IsPrivateShopItemPriceList():
	global g_itemPriceDict
	if g_itemPriceDict:
		return True
	else:
		return False

def IsBuildingPrivateShop():
	global g_isBuildingPrivateShop
	if player.IsOpenPrivateShop() or g_isBuildingPrivateShop:
		return True
	else:
		return False

def SetPrivateShopItemPrice(itemVNum, itemPrice):
	global g_itemPriceDict
	g_itemPriceDict[int(itemVNum)]=itemPrice
	
def GetPrivateShopItemPrice(itemVNum):
	try:
		global g_itemPriceDict
		return g_itemPriceDict[itemVNum]
	except KeyError:
		return 0
		
def UpdateADBoard():	
	for key in g_privateShopAdvertisementBoardDict.keys():
		g_privateShopAdvertisementBoardDict[key].Show()
		
def DeleteADBoard(vid):
	if not g_privateShopAdvertisementBoardDict.has_key(vid):
		return
			
	del g_privateShopAdvertisementBoardDict[vid]
		

class PrivateShopAdvertisementBoard(ui.ThinBoard):
	def __init__(self):
		ui.ThinBoard.__init__(self, "UI_BOTTOM")
# OFFLINE_SHOPS_METGUIDE
		self.shopAdvertismentBoardSeen = []
# END_OFFLINE_SHOPS_METGUIDE
		self.vid = None
		self.__MakeTextLine()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def __MakeTextLine(self):
		self.textLine = ui.TextLine()
		self.textLine.SetParent(self)
		self.textLine.SetWindowHorizontalAlignCenter()
		self.textLine.SetWindowVerticalAlignCenter()
		self.textLine.SetHorizontalAlignCenter()
		self.textLine.SetVerticalAlignCenter()
		self.textLine.Show()

# OFFLINE_SHOPS_METGUIDE
	def Open(self, vid, text):
		global g_shopAdvertismentBoardSeen
		self.vid = vid
	
		if vid in g_shopAdvertismentBoardSeen:
			text = "(Vãzut) " + text
	
		self.textLine.SetText(text)
		self.textLine.UpdateRect()
		self.SetSize(len(text) * 6 + 10 * 2, 20)
		self.Show()
	
		g_privateShopAdvertisementBoardDict[vid] = self
# END_OFFLINE_SHOPS_METGUIDE

# OFFLINE_SHOPS_METGUIDE
	def OnMouseLeftButtonUp(self):
		global g_shopAdvertismentBoardSeen
		if not self.vid:
			return
		net.SendOnClickPacket(self.vid)
		if self.vid != player.GetMainCharacterIndex():
			self.textLine.SetPackedFontColor(SHOP_VISIT_COLOR)
			g_shopAdvertismentBoardSeen[self.vid] = True
			text = self.textLine.GetText()
			if "(Vãzut)" not in text:
				text = "(Vãzut) " + text
				self.textLine.SetText(text)
				self.textLine.UpdateRect()
				self.SetSize(len(text) * 6 + 10 * 2, 20)
		return True
# END_OFFLINE_SHOPS_METGUIDE

# OFFLINE_SHOPS_METGUIDE
	def OnUpdate(self):
		global g_shopAdvertismentBoardSeen
		if not self.vid:
			return
	
		if systemSetting.IsShowSalesText():
			self.Show()
			x, y = chr.GetProjectPosition(self.vid, 220)
			self.SetPosition(x - self.GetWidth() / 2, y - self.GetHeight() / 2)
	
			if self.vid in g_shopAdvertismentBoardSeen:
				self.textLine.SetPackedFontColor(SHOP_VISIT_COLOR)
				text = self.textLine.GetText()
				if "(Vãzut)" not in text:
					text = "(Vãzut) " + text
					self.textLine.SetText(text)
					self.textLine.UpdateRect()
					self.SetSize(len(text) * 6 + 10 * 2, 20)
		else:
			for key in g_privateShopAdvertisementBoardDict.keys():
				if player.GetMainCharacterIndex() == key:
					g_privateShopAdvertisementBoardDict[key].Show()
					x, y = chr.GetProjectPosition(player.GetMainCharacterIndex(), 220)
					g_privateShopAdvertisementBoardDict[key].SetPosition(x - self.GetWidth() / 2, y - self.GetHeight() / 2)
				else:
					g_privateShopAdvertisementBoardDict[key].Hide()
# END_OFFLINE_SHOPS_METGUIDE

class PrivateShopBuilder(ui.ScriptWindow):

	def __init__(self):
		#print "NEW MAKE_PRIVATE_SHOP_WINDOW ----------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)

		self.__LoadWindow()
		self.itemStock = {}
		self.tooltipItem = None
		self.priceInputBoard = None
# OFFLINE_SHOPS_METGUIDE
		self.days = 0
# END_OFFLINE_SHOPS_METGUIDE
		self.title = ""

	def __del__(self):
		#print "------------------------------------------------------------- DELETE MAKE_PRIVATE_SHOP_WINDOW"
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PrivateShopBuilder.py")
		except:
			import exception
			exception.Abort("PrivateShopBuilderWindow.LoadWindow.LoadObject")

		try:
			GetObject = self.GetChild
			self.nameLine = GetObject("NameLine")
			self.itemSlot = GetObject("ItemSlot")
			self.btnOk = GetObject("OkButton")
			self.btnClose = GetObject("CloseButton")
			self.titleBar = GetObject("TitleBar")
		except:
			import exception
			exception.Abort("PrivateShopBuilderWindow.LoadWindow.BindObject")

		self.btnOk.SetEvent(ui.__mem_func__(self.OnOk))
		self.btnClose.SetEvent(ui.__mem_func__(self.OnClose))
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.OnClose))

		self.itemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.OnSelectEmptySlot))
		self.itemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectItemSlot))
		self.itemSlot.SetOverInItemEvent(ui.__mem_func__(self.OnOverInItem))
		self.itemSlot.SetOverOutItemEvent(ui.__mem_func__(self.OnOverOutItem))

	def Destroy(self):
		self.ClearDictionary()

		self.nameLine = None
		self.itemSlot = None
		self.btnOk = None
		self.btnClose = None
		self.titleBar = None
		self.priceInputBoard = None

# OFFLINE_SHOPS_METGUIDE
	def Open(self, title,days):

		self.days = days
		self.title = title
# END_OFFLINE_SHOPS_METGUIDE

		if len(title) > 25:
			title = title[:22] + "..."

		self.itemStock = {}
		shop.ClearPrivateShopStock()
		self.nameLine.SetText(title)
		self.SetCenterPosition()
		self.Refresh()
		self.Show()

		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = True

	def Close(self):
		global g_isBuildingPrivateShop
		g_isBuildingPrivateShop = False

		self.title = ""
		self.itemStock = {}
		shop.ClearPrivateShopStock()
		self.Hide()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Refresh(self):
		getitemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setitemVNum=self.itemSlot.SetItemSlot
		delItem=self.itemSlot.ClearSlot

		for i in xrange(shop.SHOP_SLOT_COUNT):

			if not self.itemStock.has_key(i):
				delItem(i)
				continue

			pos = self.itemStock[i]

			itemCount = getItemCount(*pos)
			if itemCount <= 1:
				itemCount = 0
			setitemVNum(i, getitemVNum(*pos), itemCount)

		self.itemSlot.RefreshSlot()

# OFFLINE_SHOPS_METGUIDE
	def ReadFilePrice(self,vnum,count):
		d = "shops"
		if not os.path.exists(d):
			os.makedirs(d)
		oldPrice=0
		n=d+"/"+str(vnum)+"_"+str(count)+".txt"
		if os.path.exists(n):
			fd = open( n,'r')
			oldPrice=int(fd.readlines()[0])
			
		return oldPrice

	def SaveFilePrice(self,vnum,count,price):
		d = "shops"
		if not os.path.exists(d):
			os.makedirs(d)
		n=d+"/"+str(vnum)+"_"+str(count)+".txt"
		f = file(n, "w+")
		f.write(str(price))
		f.close()
# END_OFFLINE_SHOPS_METGUIDE

	def OnSelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			mouseModule.mouseController.DeattachObject()

			if player.SLOT_TYPE_INVENTORY != attachedSlotType and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedSlotType:
				return
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
# OFFLINE_SHOPS_METGUIDE
			count = player.GetItemCount(attachedInvenType, attachedSlotPos)
# END_OFFLINE_SHOPS_METGUIDE
			itemVNum = player.GetItemIndex(attachedInvenType, attachedSlotPos)
			item.SelectItem(itemVNum)

			if item.IsAntiFlag(item.ANTIFLAG_GIVE) or item.IsAntiFlag(item.ANTIFLAG_MYSHOP):
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.PRIVATE_SHOP_CANNOT_SELL_ITEM)
				return

			priceInputBoard = uiCommon.MoneyInputDialog()
			priceInputBoard.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_PRICE_DIALOG_TITLE)
			priceInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrice))
			priceInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrice))
# OFFLINE_SHOPS_METGUIDE
			priceInputBoard.SetMaxLength(14)
# END_OFFLINE_SHOPS_METGUIDE
			priceInputBoard.Open()

# OFFLINE_SHOPS_METGUIDE
			itemPrice=self.ReadFilePrice(itemVNum,count)# OFFLINE_SHOPS_METGUIDE
# END_OFFLINE_SHOPS_METGUIDE

			if itemPrice>0:
				priceInputBoard.SetValue(itemPrice)
			
			self.priceInputBoard = priceInputBoard
			self.priceInputBoard.itemVNum = itemVNum
			self.priceInputBoard.sourceWindowType = attachedInvenType
			self.priceInputBoard.sourceSlotPos = attachedSlotPos
			self.priceInputBoard.targetSlotPos = selectedSlotPos

	def OnSelectItemSlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			snd.PlaySound("sound/ui/loginfail.wav")
			mouseModule.mouseController.DeattachObject()

		else:
			if not selectedSlotPos in self.itemStock:
				return

			invenType, invenPos = self.itemStock[selectedSlotPos]
			shop.DelPrivateShopItemStock(invenType, invenPos)
			snd.PlaySound("sound/ui/drop.wav")

			del self.itemStock[selectedSlotPos]

			self.Refresh()

	def AcceptInputPrice(self):

		if not self.priceInputBoard:
			return True

		text = self.priceInputBoard.GetText()

		if not text:
			return True

		if not text.isdigit():
			return True

		if long(text) <= 0:# OFFLINE_SHOPS_METGUIDE
			return True

		attachedInvenType = self.priceInputBoard.sourceWindowType
		sourceSlotPos = self.priceInputBoard.sourceSlotPos
		targetSlotPos = self.priceInputBoard.targetSlotPos

		for privatePos, (itemWindowType, itemSlotIndex) in self.itemStock.items():
			if itemWindowType == attachedInvenType and itemSlotIndex == sourceSlotPos:
				shop.DelPrivateShopItemStock(itemWindowType, itemSlotIndex)
				del self.itemStock[privatePos]

		price = int(self.priceInputBoard.GetText())

		if IsPrivateShopItemPriceList():
			SetPrivateShopItemPrice(self.priceInputBoard.itemVNum, price)

		shop.AddPrivateShopItemStock(attachedInvenType, sourceSlotPos, targetSlotPos, price)
# OFFLINE_SHOPS_METGUIDE
		count = player.GetItemCount(attachedInvenType, sourceSlotPos)
		vnum = player.GetItemIndex(attachedInvenType, sourceSlotPos)
		self.SaveFilePrice(vnum,count,price)
# END_OFFLINE_SHOPS_METGUIDE
		self.itemStock[targetSlotPos] = (attachedInvenType, sourceSlotPos)
		snd.PlaySound("sound/ui/drop.wav")

		self.Refresh()		

		#####

		self.priceInputBoard = None
		return True

	def CancelInputPrice(self):
		self.priceInputBoard = None
		return True

	def OnOk(self):

		if not self.title:
			return

		if 0 == len(self.itemStock):
			return

		shop.BuildPrivateShop(self.title,self.days)# OFFLINE_SHOPS_METGUIDE
		self.Close()

	def OnClose(self):
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnOverInItem(self, slotIndex):

		if self.tooltipItem:
			if self.itemStock.has_key(slotIndex):
				self.tooltipItem.SetPrivateShopBuilderItem(*self.itemStock[slotIndex] + (slotIndex,))

	def OnOverOutItem(self):

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
