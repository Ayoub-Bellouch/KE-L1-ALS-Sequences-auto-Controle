# def ALS(commALS):
#     print("start: collectALS")
#     ALS = dict()
#     ALS["time"] = datetime.datetime.utcnow() + timedelta(hours=1)
#     # ALS["time"] = datetime.datetime.utcnow()
    
#     # ## SS ## Simulation !
#     # ALS.extend([123, 87, "Model X", 26.33])
#     # return ALS
#     # ## SS ##
    
#     # Static Logic !
# #     EntryLif = commALS.Read("LI106_GLASS_counter").Value
#     # Dynamic Logic !
#     ALS["EntryLif_stats"] = commALS.Read("LI106_GLASS_counter_stats").Value
#     # ALS["EntryLif_stats_ls"] = commALS.Read("LI106_GLASS_counter_stats_ls").Value
    
#     # Static Logic !
# #     Exitlif = commALS.Read("LI202_SENDING_GLASS_counter").Value
#     # Dynamic Logic !
#     ALS["Exitlif_stats"] = commALS.Read("LI202_SENDING_GLASS_counter_stats").Value
#     # ALS["Exitlif_stats_ls"] = commALS.Read("LI202_SENDING_GLASS_counter_stats_ls").Value
    
#      # Static Logic !
#     ALS["LiveALS_ModelName"] = commALS.Read("RCP_KINEMATIC_ACTUAL.NAME").Value
    
#     # Static Logic !
#     ALS["LiveALS_ModelCycle_Time"]  = commALS.Read("CV109_W.RCP.CYCLE_TIME").Value
    
#     print("end: collecALS \n Values : ", ALS)
#     return(ALS)
