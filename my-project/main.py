# pyright: basic
from manim import *
import numpy
from enum import Enum
from numpy.lib.scimath import sqrt, power


class intro(Scene):
    def construct(self):
        metadata_group = Group()

        date = Text("24-5-2025", font_size=14)
        project = Text("Project Embedded Systems", font_size=14)
        metadata_group.add(date, project)
        metadata_group.to_corner(UR)
        metadata_group.arrange(DOWN)

        self.add(metadata_group.to_corner(UR))

        box = Rectangle(color="#FFFFFF", width=6)
        box.add(Text("UART Protocol", font="Noto Serif"))
        self.add(box)
        self.wait(3);
        
        protocol = Rectangle(color="#F9F9F9")
        protocol.set_opacity(0);
        self.remove(metadata_group)
        self.add(protocol)
        self.play(box.animate.next_to(box, UP));
        self.wait(1)
        protocol.set_opacity(1);
        self.add(protocol)


class protocol_view(Scene):

    def construct(self):
        test = graphFunc([1])

        graph = FunctionGraph(function=test.displayFunction, x_range=[0,20]);
        self.add(graph)


class drawingstate_enum(Enum):
    low = 1 
    to_high = 1.5
    high = 2
    to_low = 1.2
    
        
class graphFunc:
    to_send = [1,2,3,4,5]
    value_high = 1
    value_low = 0

    def __init__(self, array):
        self.list = array


    def to_higher_formula(self, t, start_time, len):
        calc_time = t - start_time
        range = self.value_high - self.value_low;

        to_the_power_of = sqrt(self.value_high)/len
        ret = power(calc_time, to_the_power_of);

        return ret


    def to_lower_formula(self, t, start_time, len):
        calc_time = t - start_time;
        range = self.value_high - self.value_low;

        unit = range / len+1
        inverse_of_calc_time = len - calc_time;

        return inverse_of_calc_time / unit;


    def string_to_binary(self, String: str):
        return int.from_bytes(String.encode(), 'big')


    def drawbyte(self, t_in: numpy.float64, t_start, len, byte: int):

        t_calc = t_in - t_start
        bit_duration = len/10
    

        current_bit_pos = (t_calc / bit_duration).astype(int)
        
        print("t_in: ", t_in, " t_start" , t_start , " tcalc: ", t_calc, " bit_dur: ", bit_duration , current_bit_pos, "\r\n")

        if current_bit_pos == 0:
            return self.value_low

        if current_bit_pos == 10:
            return self.value_high

        # str precede width "0b" and the first bit isn't b
        current_bit_pos += 1;
        current_bit = byte[current_bit_pos]
        next_bit = byte[current_bit_pos+1]
        prev_bit = byte[current_bit_pos-1]


        if (prev_bit == current_bit  == next_bit): # no egde detection required
            if current_bit == 1:
                print("hi\r\n")
                return self.value_high
            else:
                print("no?\r\n")
                return self.value_low
        
        # below edge detection
        upline_lenght_in_precent = 2
        downline_lenght_in_precent = 2

        bit_progression_in_time = t_calc%bit_duration

        upline_lenght   = 100 / upline_lenght_in_precent * bit_duration;
        upline_threshold = upline_lenght;

        downline_lenght =   100 / downline_lenght_in_precent * bit_duration;
        downline_threshold = bit_duration - downline_lenght ;

        if prev_bit != current_bit:
            if  (bit_progression_in_time < upline_threshold):
                return self.to_higher_formula(t_in, t_start + current_bit_pos*bit_duration, upline_lenght)

        elif  current_bit != next_bit:
            if  (bit_progression_in_time > downline_threshold):
                return self.to_lower_formula( t_in, t_start + current_bit_pos*bit_duration, downline_lenght)

        # okay if the code come here there is a bug in my logic


    def displayFunction(self, t):
        byte_duration = 4   
        start_of_loop = t-t%byte_duration
        return self.drawbyte(t, start_of_loop, byte_duration, self.string_to_binary("a"));


