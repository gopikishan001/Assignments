#!/usr/bin/env python

import rospy 
from std_msgs.msg import String
from csv import writer


class scheduler :

	# variables for storing and managing info 
	def __init__(self) :

		rospy.Subscriber('/order', String ,self.order_callback)
		
		# order list [order time , recipe , current cooking stage , order id ]
		self.order_list = []

		# maintains saute occupied status [status , release time , ocupied by order id 
		self.saute_status = [[False, 0 , 0], [False , 0 , 0], [False, 0 , 0]]
		self.saute_list = []   # keeps info of order kept in saute
		self.time = 0		   # instance of time

		# time line for recepies ( cooking stages )
		self.time_info = {  0 :[5,"Picking up a new bowl"],
							1 : [5, "Picking up ingredients "], 
							2 : [5 , "Placing bowl on stove "] , 
							3 : [60,"saute"] , 
							4 : [5,"Picking up ingredients "] , 
							5 : [5 , "Placing bowl on stove "] , 
							6 : [120, "saute"] , 
							7 : [5,"Add ingredients "] , 
							8 : [60,"saute"] , 
							9 : [5,"Removing bowl "]}
		self.order_id = 0
		self.order_active_status = []

	def order_callback(self, msg) :
		ros_string = msg.data.split(":")
		for order_string in ros_string :
			info = order_string.split("-")
			self.order_list.append([int(info[0]) , info[1].replace("_" , " ") , 0 , self.order_id])
			self.order_id += 1


	def schedule(self) :

		for order in range(len(self.order_list)) :

			if self.order_list[order][0] <= self.time :
				if self.order_list[order][2] <= 9 :
				
					if self.order_list[order][3] in self.order_active_status :  

						if self.time_info[self.order_list[order][2]][1]  == "saute" :
							if order in self.saute_list :
								continue

							for saute in (range(len(self.saute_status))) :
								if self.saute_status[saute][0] == False :

									# updating values and creating data for log
									
									self.saute_status[saute] = [True, self.time + self.time_info[self.order_list[order][2]][0], order ]
									self.saute_list.append(order )

									order_no     = str( self.order_list[order][3] + 1)
									receive_time = str( self.order_list[order][0] ) + " sec"
									dish_name    = self.order_list[order][1]
									start_time = str(self.time) + " sec" 
									end_time   = str(self.time + self.time_info[self.order_list[order][2] ][0] ) + " sec"
									operation  = self.time_info[self.order_list[order][2]][1] + " on saute_" + str(saute)

									self.time += 5
									self.write_log([order_no, receive_time, dish_name, start_time, end_time, operation])

									return

						else :

							# updating values and creating data for log

							start_time = str(self.time) + " sec" 

							self.time += self.time_info[self.order_list[order][2]][0]
							self.order_list[order][2] += 1

							order_no     = str( self.order_list[order][3] + 1)
							receive_time = str( self.order_list[order][0] ) + " sec"
							dish_name    = self.order_list[order][1]
							end_time   = str(self.time ) + " sec"
							operation  = self.time_info[self.order_list[order][2] - 1][1] 

							self.write_log([order_no, receive_time, dish_name, start_time, end_time, operation])

							return

					elif len(self.order_active_status) < 3:
						self.order_active_status.append(self.order_list[order][3])
						return

				else :

					if self.order_list[order][3] in self.order_active_status :
						self.order_active_status.remove(self.order_list[order][3])
						return

		if len(self.order_list) > 0:
			self.time += 1

	# checking if saute done and updating saute status
	def saute_check(self) :
		for i in range(len(self.saute_status)) :
			if self.saute_status[i][0] == True :
				if self.time >= self.saute_status[i][1] :
					self.saute_status[i][0] = False 
					self.saute_list.remove(self.saute_status[i][2])
					self.order_list[self.saute_status[i][2]][2] += 1

	# apending data to CSV as log file
	def write_log(self, data) :
		with open('log.csv', 'a') as f_object:
			writer_object = writer(f_object)
			writer_object.writerow(data)
			f_object.close()

		print(data)


if __name__ == "__main__" :

	obj = scheduler()
	obj.write_log(["Order Number", "Order Received Time", "Dish", "Start Time", "End Time", "Operation" ])
	
	rospy.init_node('order_scheduler')

	rate = rospy.Rate(60)

	while not rospy.is_shutdown():
		obj.schedule()
		obj.saute_check()
		rate.sleep()
