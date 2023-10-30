import pyodbc
import pandas as pd

class NewSKU():
    global cur,CATEGORY
    CATEGORY = 'Combo'
    
    conn = ("""driver={SQL Server};server={{ Database Port }};database={{ Database Name }};
        trusted_connection=no;UID=CCS02;PWD=Pass@1234;IntegratedSecurity = true;""")
    conx = pyodbc.connect(conn)
    cur = conx.cursor()

    def reading_csv(self):

        Dataset = pd.read_csv(r'C:\Users\Emiza\Desktop\Dummy_file.csv')
        Dict_data = Dataset.to_dict(orient='records')
        for x in range(len(Dict_data)):
            TABLE_DATA = Dict_data[x]
            # print(TABLE_DATA)
            PARENT_SKU = str(TABLE_DATA["PARENT SKU"])              # Parent SKU CODE
            # print(PARENT_SKU)
            DESCRIPTION = str(TABLE_DATA["DESCRIPTION"])            # Decription of SKU
            # print(DESCRIPTION)
            Component1 = str(TABLE_DATA["Component_1"])             # Component of SKU
            # print(Component_1_SKU)
            Owner_name = str(TABLE_DATA["Owner Name"])              # Owner Name 
            # print(Owner_name)
            Component_1_QTY = str(TABLE_DATA["Component_1_QTY"])    # Component QTY of SKU
            # print(Component2)
            self.check_Category(PARENT_SKU,Component1,DESCRIPTION,CATEGORY,Owner_name,Component_1_QTY)


    def check_Category(self,PARENT_SKU,Component1,DESCRIPTION,CATEGORY,Owner_name,Component_1_QTY):  # Category
        
        Component_1_QTY = Component_1_QTY

        SELECT_QUERY1 = "SELECT OwnerId FROM Owners WHERE Name =  '"+Owner_name+"'"
        exe_O = cur.execute(SELECT_QUERY1)
        data1 = exe_O.fetchall()
        Owner_ID = data1[0][0]
        # print(Owner_ID)
        
        SELECT_QUERY2 = "SELECT OwnerCategoryId FROM OwnerCategories WHERE Name = '"+str(CATEGORY)+"' and OwnerId = '"+str(Owner_ID)+"'"
        exe1 = cur.execute(SELECT_QUERY2)
        data = exe1.fetchall()
        # print(data)
        
        if not data:
            INSERT_QUERY1 = "INSERT INTO [dbo].[OwnerCategories]([OwnerId],[Name],[SerializedFlag],[LotFlag],[CreatedBy],[CreatedDate])VALUES('"+str(Owner_ID)+"','"+str(CATEGORY)+"','N','N','EmizaSupport',GETDATE())"
            exe2 = cur.execute(INSERT_QUERY1)
            print(cur.rowcount, "Category Added")
            cur.commit()  

            SELECT_QUERY3 = "SELECT OwnerCategoryId FROM OwnerCategories WHERE Name = '"+CATEGORY+"'"
            exe3 = cur.execute(SELECT_QUERY3)
            data3 = exe3.fetchall()
            CategoryID = data3[0][0]
            print("Category Created ",CATEGORY,":",CategoryID)
            self.checkItemID(CategoryID,PARENT_SKU,Component1,DESCRIPTION,Component_1_QTY)
        else:
            CategoryID = data[0][0]
            print("Catgeory Already Available = ",CATEGORY,":",CategoryID)
            self.checkItemID(CategoryID,PARENT_SKU,Component1,DESCRIPTION,Component_1_QTY)
            

    def checkItemID(self,CategoryID,PARENT_SKU,Component1,DESCRIPTION,Component_1_QTY):   #Parent SKU 

        Component_1_QTY = Component_1_QTY

        SELECT_QUERY4 = "SELECT ItemId FROM ItemMaster WHERE ItemId ='"+PARENT_SKU+"'"
        exe_NO = cur.execute(SELECT_QUERY4)
        data4 = exe_NO.fetchall()

        if not data4:
            
            INSERT_QUERY2 = "INSERT INTO [dbo].[ItemMaster] ([ItemId],[OwnerCategoryId],[Description],[CreatedBy],[CreatedDate],[CFT])VALUES('"+str(PARENT_SKU)+"','"+str(CategoryID)+"','"+str(DESCRIPTION)+"','EmizaSupport',GETDATE(),'1')"
            exe3 = cur.execute(INSERT_QUERY2)
            print(PARENT_SKU, "Parent SKU is Added")
            cur.commit()  

            SELECT_QUERY5 = "SELECT ItemId FROM ItemMaster WHERE ItemId ='"+PARENT_SKU+"'"
            exe_O = cur.execute(SELECT_QUERY5)
            data4 = exe_O.fetchall()
            Item_ID = data4[0][0]
            print("Parent SKU Created =",Item_ID)
            self.Create_ITEM_BOM(CategoryID,PARENT_SKU,Component1,Component_1_QTY)
        else:
            Item_ID = data4[0][0]
            print("Parent SKU is already Available =",Item_ID)
            self.Create_ITEM_BOM(CategoryID,PARENT_SKU,Component1,Component_1_QTY)

    def Create_ITEM_BOM(self,CategoryID,PARENT_SKU,Component1,Component_1_QTY):       #Components

        SELECT_QUERY6 = "SELECT ItemId FROM ItemMaster WHERE ItemId ='"+Component1+"'"
        # print(SELECT_QUERY6)
        exe_u = cur.execute(SELECT_QUERY6)
        data5 = exe_u.fetchall()
        # print(data5)

        if not data5:
            print(Component1,"Component is not available in Database\n")
        else:
            SELECT_QUERY7 = "SELECT ItemId FROM ItemBOM WHERE ItemId = '"+PARENT_SKU+"'AND ComponentId = '"+Component1+"'"
            # print(SELECT_QUERY7)
            exe5 = cur.execute(SELECT_QUERY7)
            data6 = exe5.fetchall()
            # print(data6)

            if not data6:
                INSERT_QUERY3 = "INSERT INTO [dbo].[ItemBOM]([OwnerCategoryId],[ItemId],[ComponentId],[PiecesRequired],[CreatedBy],[CreatedDate])VALUES('"+str(CategoryID)+"','"+str(PARENT_SKU)+"','"+str(Component1)+"','"+str(Component_1_QTY)+"','EmizaSupport',GETDATE())"
                # print(INSERT_QUERY3)
                exe4 = cur.execute(INSERT_QUERY3)
                print(PARENT_SKU, "Combo Added for",Component1,"with",Component_1_QTY,"Quantity.\n")
                cur.commit()
            else:
                PARENT_SKU = data6[0][0]
                print(PARENT_SKU.strip(),"Combo is already created for",Component1,"\n")

a1 = NewSKU()
a1.reading_csv()
