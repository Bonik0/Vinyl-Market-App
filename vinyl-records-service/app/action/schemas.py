from core.schemas import VinylRecordID, VinylRecordOut, SellerInfoOut




class VinylRecordWithSellerOut(VinylRecordOut):
    seller : SellerInfoOut