class Settings:
    def __init__(self, width:int, height:int, minRegionWidth:int, minRegionHeight:int, minRoomWidth:int, minRoomHeight:int, corridorWidth:int, roomMargin:int, splitBias=0.6, seed=None):
        self.width = width
        self.height = height
        self.minRegionWidth = minRegionWidth
        self.minRegionHeight = minRegionHeight
        self.minRoomWidth = minRoomWidth
        self.minRoomHeight = minRoomHeight
        self.corridorWidth = corridorWidth
        self.roomMargin = roomMargin
        self.splitBias = splitBias
        self.seed = seed

