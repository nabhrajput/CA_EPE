import txt_Converter as conv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sys
try:
    with open('Log_File.txt', 'w') as output_file:
        sys.stdout = output_file
        class Router:
            def __init__(self, router_id):
                self.router_id = router_id
                self.input_buffer = []
                self.crossbar = []
                self.switch_allocator = []

            def isempty(self):
                if((len(self.input_buffer) == 0) and (len(self.switch_allocator) == 0) and (len(self.crossbar) == 0)):
                    return True
                return False

            def __str__(self):
                s = ""
                s += f"Router ID : {self.router_id} \n"
                if(self.input_buffer != []):
                    s += f"Input Buffer Value : {self.input_buffer} \n"
                if(self.input_buffer == []):
                    s += f"Input Buffer Value : None \n"
                if(self.switch_allocator != []):
                    s += f"Switch Allocator Value : {self.switch_allocator} \n"
                if(self.switch_allocator == []):
                    s += f"Switch Allocator Value : None \n"
                if(self.crossbar != []):
                    s += f"CrossBar Value : {self.crossbar} \n"
                if(self.crossbar == []):
                    s += f"CrossBar Value : None \n"
                return s

            def inject(self,flit_details):
                self.input_buffer.append(flit_details)

            def receive(self):
                if(self.crossbar != []):
                    self.crossbar.pop(0)
                if(self.switch_allocator != []):
                    val = self.switch_allocator.pop(0)
                    self.crossbar.append(val)
                if(self.input_buffer != []):
                    val = self.input_buffer.pop(0)
                    self.switch_allocator.append(val)

            def is_ready_to_receive(self,des):
                if(int(self.router_id) == int(des) and self.crossbar != []):
                    return True
                return False

            def getflit(self): #returns flit details
                if(self.crossbar != []):
                    return self.crossbar[0]
                if(self.switch_allocator != []):
                    return self.switch_allocator[0]
                if(self.input_buffer != []):
                    return self.input_buffer[0]

            def update(self,next_id,allrouter):
                nextrouter = allrouter[next_id]
                print(f"This = {self.router_id} , Next = {nextrouter.router_id}")
                if(len(self.crossbar) != 0):
                    val = self.crossbar.pop(0)
                    nextrouter.input_buffer.append(val)

                if(len(self.switch_allocator) != 0):
                    val = self.switch_allocator.pop(0)
                    self.crossbar.append(val)

                if(len(self.input_buffer) != 0):
                    val = self.input_buffer.pop(0)
                    self.switch_allocator.append(val)

                print(f"{self.router_id} Updated")

            def is_destination_flit(self,des):
                if(self.router_id == int(des)):
                    return True
                return False

        if __name__ == '__main__':
            def xy1(flit_details,curr):
                dest=int(flit_details[2])
                curr_row=curr//3
                dest_row=dest//3
                curr_col=curr%3
                dest_col=dest%3
                next_id=0
                if(curr_col==dest_col):
                    if(curr_row==dest_row):
                        next_id= dest
                    elif(curr_row<dest_row):
                        next_id= (curr+3)
                    else:
                        next_id= (curr-3)
                else:
                    if(curr_col<dest_col):
                        next_id= (curr+1)
                    else:
                        next_id= curr-1
                        
                return next_id
            
            def yx1(flit_details,curr):
                dest = int(flit_details[2])
                curr_row = curr // 3
                dest_row = dest // 3
                curr_col = curr % 3
                dest_col = dest % 3
                next_id = 0

                # First, move along the Y-axis
                if curr_row < dest_row:
                    next_id = (curr + 3)
                elif curr_row > dest_row:
                    next_id = (curr - 3)
                else:
                    # If rows are the same, move along the X-axis
                    if curr_col < dest_col:
                        next_id = (curr + 1)
                    elif curr_col > dest_col:
                        next_id = (curr - 1)
                    else:
                        # If both rows and columns are the same, stay in the current router
                        next_id = curr

                return next_id
            
            def total_cycles_taken(all_routers,flit_details,algo):
                curr_router = all_routers[int(flit_details[0])]
                des_router = all_routers[int(flit_details[1])]
                cnt = 3
                while(curr_router != des_router):
                    curr = int(curr_router.router_id)
                    next_id = int(xy1(flit_details,curr)) if (algo == 0) else int(yx1(flit_details,curr))
                    curr_router = all_routers[next_id]
                    cnt += 3
                return cnt
            
            def ispresent(clock,traffic_file):
                for i in range(0,len(traffic_file)):
                    if(clock == int(traffic_file[i][0])):
                        return traffic_file[i]
                    
                return []
            
            def all_empty(all_routers):
                i = 0
                while(i < len(all_routers)):
                    if(not all_routers[i].isempty()):
                        return False
                    
                    i += 1

                return True
            
            def is_valid_flit_type(flit):
                if len(flit) != 32:
                    print("Length of Flits is not 32")
                    return False
                
                return all(bit in '01' for bit in flit)
            
            def bubble_sort(lst,n):
                for i in range(n):
                    for j in range(n-i-1):
                        if int(lst[j][0]) > int(lst[j+1][0]):
                            lst[j], lst[j+1] = lst[j+1], lst[j]

            def check_last_two_digits(temp1, temp2):
                return temp1[3][-2:] == temp2[3][-2:]
            try:
                flagSarva = 0
                conv.run()
                with open('traffic.txt', 'r') as file:
                    lines = file.readlines()
                    eachline2 = []
                    line_number = 1  

                    for i in range(0, len(lines), 3):
                        temp1 = lines[i].strip().split()
                        temp2 = lines[i + 1].strip().split()
                        temp3 = lines[i + 2].strip().split()

                        if len(temp1) != 4 or len(temp2) != 4 or len(temp3) != 4:
                            print(f"Error in lines {line_number}, {line_number + 1}, {line_number + 2}: Invalid number of elements in the line.")
                            flagSarva = 1

                        src1, des1, flit1 = temp1[1], temp1[2], temp1[3]
                        src2, des2, flit2 = temp2[1], temp2[2], temp2[3]
                        src3, des3, flit3 = temp3[1], temp3[2], temp3[3]

                        if src1 == des1 or src2 == des2 or src3 == des3:
                            print(f"Error in lines {line_number}, {line_number + 1}, {line_number + 2}: Source can't be the same as the destination.")
                            flagSarva = 1

                        if (int(src1) not in range(0,9)) or (int(src2) not in range(0,9)) or (int(src3) not in range(0,9)) or (int(des1) not in range(0,9)) or (int(des2) not in range(0,9)) or(int(des3) not in range(0,9)):
                            print(f"Error in lines {line_number}, {line_number + 1}, {line_number + 2}: Invalid Router ID")
                            flagSarva = 1  

                        if (not is_valid_flit_type(flit1)) or (not is_valid_flit_type(flit2)) or (not is_valid_flit_type(flit3)):
                            print(f"Error in lines {line_number}, {line_number + 1}, {line_number + 2}: Invalid flit type.")
                            flagSarva = 1

                        if check_last_two_digits(temp1, temp2) or check_last_two_digits(temp2, temp3) or check_last_two_digits(temp1, temp3):
                            print(f"Error in lines {line_number}, {line_number + 1}, {line_number + 2}: Last two digits match.")
                            flagSarva = 1
                        
                        if flagSarva==1:
                            exit()

                        eachline2.extend([temp1, temp2, temp3])
                        line_number += 3

            except FileNotFoundError:
                print("Error: File 'traffic.txt' not found.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            try:
                with open('delays.txt','r') as file1:
                    line1 = file1.readline()
                    line1 = line1.split()
                    line2 = []
                    delay_dic = {0 : 'Input Buffer' , 1 : 'Switch Allocator' , 2 : 'CrossBar' }
                    for i in range(0,len(line1)):
                        line2.append(float(line1[i]))
                        if line2[i] < 0:
                            print(f"Error : You have provided a negative value in delays file at {delay_dic[i]}")
                            exit()

            except FileNotFoundError:
                print("Error: File 'delays.txt' not found.")
                exit()
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                exit()

            traffic_file = eachline2
            delay_file = line2

            buffer_delay = delay_file[0]
            sa_delay = delay_file[1]
            xbar_delay = delay_file[2]

            all_routers = {i : Router(i) for i in range(0,9)}

            period = max(buffer_delay,sa_delay,xbar_delay)
            
            # print("Enter 0 to run in XY & 1 to run in YX ")
            # algo = int(input())
            algo = 0 # 0 for xy | 1 for yx

            total = 0
            flit_time = []
            bubble_sort(traffic_file,len(traffic_file))

            clock_wise_flits = {}
            clock = 1
            lastclock = int(traffic_file[len(traffic_file) - 1][0])
            while(clock <= lastclock):
                flits_on_that_clock = []
                for i in range(0,len(traffic_file)):
                    if(int(traffic_file[i][0]) == clock):
                        flits_on_that_clock.append(traffic_file[i])
                if(flits_on_that_clock != []):
                    clock_wise_flits[clock] = flits_on_that_clock
                clock += 1

            clock = 1 #defining the clock
            while(clock <= lastclock or (not all_empty(all_routers))):
                if(clock in clock_wise_flits): # indicator that flit has to be injected in this cycle
                    flits_on_that_clock = clock_wise_flits[clock] #list of flits to be injected on this clock
                    
                    i = 8
                    while(i >= 0): #to update the the routers
                        r = all_routers[i] # Rth router
                        flits_on_this_router = [] #flits to be injected on this router on this cycle
                        for j in range(0,len(flits_on_that_clock)):
                            if(i == int(flits_on_that_clock[j][1])): # router_no == flit_src
                                flits_on_this_router.append(flits_on_that_clock[j])
                        
                        #now we have number of flits to be injected at this particular source at this particular cycle
                        '''Case 1 : if the router is not empty 
                                step 1 : update the already existing flits
                                step 2 : inject the new flits
                            Case 2 : the router is already empty (there is no need for any updation)
                                step 1 : Directly Inject the flits'''
                        if(not r.isempty()): 
                            curr_flit_details = r.getflit()

                            if(r.is_destination_flit(curr_flit_details[2])):
                                r.receive()
                            else:
                                next_r = xy1(curr_flit_details,i) if (algo == 0) else yx1(curr_flit_details,i)
                                r.update(next_r,all_routers)

                            while(len(flits_on_this_router) != 0):
                                r.inject(flits_on_this_router.pop(0))
                        else:
                            while(len(flits_on_this_router) != 0):
                                r.inject(flits_on_this_router.pop(0))

                        i -=1 

                else: # indicator that flit has to be injected in this cycle (flits_on_that_clock == None)
                    print(f"No injection Done of clock = {clock}")
                    i = 8
                    while(i >= 0):
                        r = all_routers[i]

                        if(not r.isempty()):
                            curr_flit_details = r.getflit()
                            
                            if(r.is_destination_flit(int(curr_flit_details[2]))):
                                r.receive()
                            else:
                                next_r = xy1(curr_flit_details,i) if (algo == 0) else yx1(curr_flit_details,i)
                                r.update(next_r,all_routers)

                        i -= 1

                j = 0 
                while j <= 8:
                    try:
                        print(f"At clock cycle: {clock} = {all_routers[j]}")
                    except Exception as e:
                        print(f"Error printing router details: {str(e)} for value router no. = {j}")
                    j += 1

                print("---------------------------------------------------------------------------------------------------------\n")

                clock += 1
                total += period

                #emergency button
                if(clock == 20):
                    print("forcefull stop")
                    exit()


                        



            
            
            # while((not all_empty(all_routers)) or len(traffic_file) != 0):
            #     curr = ispresent(clock,traffic_file)

            #     if(curr != []): #traffic file not empty
            #         traffic_file.remove(curr)

            #         clk_cycle = int(curr[0])
            #         src = int(curr[1])
            #         des = int(curr[2])
            #         flit = curr[3]

            #         flit_details = [src,des,flit]

            #         i = 8
            #         while(i >= 0):
            #             r = all_routers[i]

            #             if(i != src):
            #                 if(not r.isempty()):
            #                     curr_flit_details = r.getflit()
            #                     if(curr_flit_details[0]>curr_flit_details[1]):
            #                         i-=1
            #                         continue
            #                     next_r = xy1(curr_flit_details,i) if (algo == 0) else yx1(curr_flit_details,i)
            #                     r.update(next_r,all_routers)

            #             else:
            #                 if(not r.isempty()):
            #                     if(src>des):
            #                         i-=1
            #                         continue
            #                     next_r = xy1(flit_details,i) if (algo == 0) else yx1(flit_details,i)
            #                     r.update(next_r,all_routers)
            #                     r.inject(flit_details)
            #                     flit_time.append(total_cycles_taken(all_routers,flit_details,algo))

            #                 else:
            #                     if(src>des):
            #                         i-=1
            #                         continue
            #                     r.inject(flit_details)
            #                     flit_time.append(total_cycles_taken(all_routers,flit_details,algo))
            
            #             i -= 1
            #         i=0
            #         while(i <=8):
            #             r = all_routers[i]

            #             if(i != src):
            #                 if(not r.isempty()):
            #                     curr_flit_details = r.getflit()
            #                     if(curr_flit_details[0]<=curr_flit_details[1]):
            #                         i+=1
            #                         continue
            #                     next_r = xy1(curr_flit_details,i) if (algo == 0) else yx1(curr_flit_details,i)
            #                     r.update(next_r,all_routers)

            #             else:
            #                 if(not r.isempty()):
            #                     if(src<=des):
            #                         i+=1
            #                         continue
            #                     next_r = xy1(flit_details,i) if (algo == 0) else yx1(flit_details,i)
            #                     r.update(next_r,all_routers)
            #                     r.inject(flit_details)
            #                     flit_time.append(total_cycles_taken(all_routers,flit_details,algo))
            #                 else:
            #                     if(src<=des):
            #                         i+=1
            #                         continue
            #                     r.inject(flit_details)
            #                     flit_time.append(total_cycles_taken(all_routers,flit_details,algo))
            
            #             i += 1
                    
            #     else:
            #         i = 8
            #         while(i >= 0):
            #             r = all_routers[i]
            #             if(not r.isempty()):
            #                 flit_details = r.getflit() #returns a list
            #                 if(flit_details[0]>flit_details[1]):
            #                     i-=1
            #                     continue
                            
            #                 if(r.is_destination_flit(flit_details[1])):
            #                     r.receive()
                
            #                 else:
            #                     next_r = xy1(flit_details,i) if (algo == 0) else yx1(flit_details,i)
            #                     r.update(next_r,all_routers)
                                    
            #             i -= 1

            #         i = 0
            #         while(i <= 8):
            #             r = all_routers[i]
            #             if(not r.isempty()):
            #                 flit_details = r.getflit() #returns a list
            #                 if(flit_details[0]<=flit_details[1]):
            #                     i+=1
            #                     continue

            #                 if(r.is_destination_flit(flit_details[1])):
            #                     r.receive()
                
            #                 else:
            #                     next_r = xy1(flit_details,i) if (algo == 0) else yx1(flit_details,i)
            #                     r.update(next_r,all_routers)
                                
            #             i += 1
                        
            #     j = 0 
            #     while j <= 8:
            #         try:
            #             print(f"At clock cycle: {clock} = {all_routers[j]}")
            #         except Exception as e:
            #             print(f"Error printing router details: {str(e)}")
            #         j += 1

            #     print("---------------------------------------------------------------------------------------------------------\n")

            #     clock += 1
            #     total += period

            
    sys.stdout = sys.__stdout__

    print("Output is stored in a file name : 'Log_File.txt'")

    c = canvas.Canvas("report.pdf", pagesize=letter)
    title = "Report File Generated By Group 40"
    title_width = c.stringWidth(title, 'Helvetica', 24) 
    title_x = (letter[0] - title_width) / 2  

    text = []
    nabh = []
    # text.append(title)
    with open('traffic.txt', 'r') as file:
        lines = file.readlines()
        eachline2 = []
        for i in range(0, len(lines)):
            temp1 = lines[i].strip().split()
            nabh.append(temp1)

    for i in range(0, len(flit_time), 3):
        packet_num = i // 3 + 1
        head_time, body_time, tail_time = flit_time[i], flit_time[i + 1], flit_time[i + 2]

        text.append(f"Head Flit of Packet number {packet_num} is taking {head_time} units to go From {nabh[i][1]}, to CrossBar of {nabh[i][2]} router")
        text.append(f"Body Flit of Packet number {packet_num} is taking {head_time-1} units to go From {nabh[i][1]}, to Switch-Allocator of {nabh[i][2]} router")
        text.append(f"Tail Flit of Packet number {packet_num} is taking {head_time-2} units to go From {nabh[i][1]}, to Input-Buffer of {nabh[i][2]} router")
        text.append("")

    text.append(f"The Total Time Taken to transfer all Packets is {total} units")
    text.append(f"The Total Clock cycles taken to transfer all Packets is {clock-1} units")
    text.append(f"The Clock Frequency of our NOC is {1/period} units")

    y_position = 650
    x_position = 15

    c.setFont("Helvetica", 24) 
    c.drawString(title_x, 750, title) 
    for line in text:
        c.setFont("Helvetica", 14) 
        c.drawString(x_position, y_position-24, line)
        y_position -= 18
    c.save()

except Exception as e:
    print(f"Error printing output location: {str(e)}")