import Shapes
import cairo
import numpy
import math

def canvas_input():
	# Takes user input to determine Size of Drawing Canvas	
	
	Length = raw_input("Enter canvas length: ")
	ulength = Length.decode(encoding='UTF-8',errors='strict')
	while True:
		if ulength.isnumeric():
			Length = float(Length)
			break
		else:
			Length = raw_input("Input Error! Please Enter Numeric Length: ")
			ulength = Length.decode(encoding='UTF-8',errors='strict')
	Width = raw_input("Enter canvas width: ")
	uwidth = Width.decode(encoding='UTF-8',errors='strict')
	while True:
		if uwidth.isnumeric():
			Width = float(Width)
			break
		else:
			Width = raw_input("Input Error! Please Enter Numeric Width: ")
			uwidth = Width.decode(encoding='UTF-8',errors='strict')

	return [Length,Width]

def draw_RegPoly(cr,poly):
	#Draws Regular Polygon onto canvas with a stroke and no fill
	poly.vertices(0)
	cr.move_to(poly.points[0][0],poly.points[0][1])
	for x in range (1,poly.num_sides):
		cr.line_to(poly.points[x][0],poly.points[x][1])
	cr.close_path()
	cr.stroke()

def draw_PENROSE(cr,tri,l):
	#Draws Penrose N-sided regular polygon onto canvas with a stroke and no fill
	
	#Checks if possible to draw with given polygon side length and offset length
	if 0 >= tri.side_length-4*l*(math.cos(tri.inter_angle)+1):
		print "INVALID"
		return
	else:
		inner_tri = Shapes.RegPoly(tri.side_length-4*l*(math.cos(tri.inter_angle)+1),tri.num_sides)
		inner_tri.set_center(tri.centerx,tri.centery)
		inner_tri.vertices(tri.offset)
		point_tri = [] 
		for y in range(tri.num_sides):
			point_tri.append(Shapes.RegPoly(l,tri.num_sides))
			point_tri[y].set_center(tri.centerx+(tri.radius-point_tri[y].radius)*math.cos(tri.angle*y \
			+tri.offset),tri.centery+(tri.radius-point_tri[y].radius)*math.sin(tri.angle*y+tri.offset))
			point_tri[y].vertices(tri.offset)
			#draw_RegPoly(cr,point_tri[y])

		#draw_RegPoly(cr,tri)
		draw_RegPoly(cr,inner_tri)
		
		cr.move_to(point_tri[0].points[tri.num_sides-1][0],point_tri[0].points[tri.num_sides-1][1])
		cr.line_to(point_tri[0].points[1][0],point_tri[0].points[1][1])	
		for x in range(1,tri.num_sides):
			a = (x+tri.num_sides-1)%tri.num_sides
			b = (x+1)%tri.num_sides
			cr.line_to(point_tri[x].points[a][0],point_tri[x].points[a][1])	
			cr.line_to(point_tri[x].points[b][0],point_tri[x].points[b][1])
		cr.close_path()
		cr.stroke()

		for z in range(tri.num_sides):
			a = (z+tri.num_sides-1)%tri.num_sides
			b = (z+1)%tri.num_sides
			angle = tri.inter_angle*(float((tri.num_sides-3))/(tri.num_sides-2) ) - \
			(tri.inter_angle)*(z)*(float(2)/(tri.num_sides-2))
			cr.move_to(inner_tri.points[b][0],inner_tri.points[b][1])
			cr.rel_line_to(l*math.sin(angle),l*math.cos(angle))
			cr.line_to(point_tri[z].points[a][0],point_tri[z].points[a][1])	
			cr.stroke()
	
def Penrose():
	Length,Width = 1000,1000
	for x in range(3,10):
		img = cairo.SVGSurface("Penrose%s.svg" %x,Length,Width)
		cr = cairo.Context(img) 
		polygon = Shapes.RegPoly(333,x)
		polygon.set_center(Length/2,Width/2)
		draw_PENROSE(cr,polygon,30)
		cr.show_page()

# Main Function
def main():
	Length, Width = canvas_input()

	sides = int(raw_input("Enter number of sides: "))
	side_l = int(raw_input("Enter Polygon side length:"))
	shape = Shapes.RegPoly(side_l,sides)
	size_check = min(Length,Width)
	while shape.radius > size_check:
		print "Shape too large!"
		side_l = int(raw_input("Enter Polygon side length:"))
		shape.set_side_len(side_l)		

	offset = int(raw_input("Enter offset: "))
	
	shape.set_center(Length/2,Width/2)		

	img = cairo.SVGSurface("Penrose%s.svg" %sides,Length,Width)
	cr = cairo.Context(img)	

	draw_PENROSE(cr,shape,offset)
	cr.show_page()	
	



#Executes Main Function
main()
