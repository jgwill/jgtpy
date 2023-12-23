class JGTChartConfig:
  def __init__(self):
    self.nb_bar_on_chart = 375
    self.jaw_line_width = 1
    self.teeth_line_width = 1
    self.lips_line_width = 1
    self.fig_ratio_x = 24
    self.fig_ratio_y = 14
    self.fdb_marker_size = 7
    self.fractal_marker_size = 6
    self.ac_signals_marker_size = 32
    self.saucer_marker_size = 16
    self.fractal_degreehigher_marker_size = 20
    self.price_peak_marker_size = 36
    self.ao_peaks_marker_size = 42
    self.fdb_signal_marker = "o"
    self.fractal_up_marker="^"
    self.fractal_up_marker_higher= "^"
    self.fractal_dn_marker_higher = "v"
    self.fractal_dn_marker = "v"
    self.ac_signal_marker="o"
    
    self.ao_peak_above_marker_higher= "^"
    self.ao_peak_bellow__marker_higher = "v"
    self.saucer_marker = "|"
    
    self.ao_upbar_color = "g"
    self.ao_dnbar_color = "r"
    self.ac_up_color = "darkgreen"
    self.ac_dn_color = "darkred"
    self.fdb_signal_buy_color = "g"
    self.fdb_signal_sell_color = "r"
    self.jaw_color = "blue"
    self.teeth_color = "red"
    self.lips_color = "green"
    self.fractal_up_color = "blue"
    self.fractal_dn_color = "blue"
    self.fractal_dn_color_higher = "blue"
    self.fractal_up_color_higher = "blue"
    self.ac_signal_buy_color = "lightgreen"
    self.ac_signal_sell_color = "yellow"
    self.saucer_buy_color = "g"
    self.saucer_sell_color= "r"
    self.price_peak_bellow_marker = "o"
    self.price_peak_above_marker = "o"
    self.price_peak_above_color = "g"
    self.price_peak_bellow_color = "r"
    
    self.ao_peak_offset_value = 0
    
    self.plot_style = "yahoo"
    self.ao_plot_type = "bar"
    self.ac_plot_type = "bar"
    

# Create an instance with default values
default_config = JGTChartConfig()

