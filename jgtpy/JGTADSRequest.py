
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTCDSRequest import JGTCDSRequest



class JGTADSRequest(JGTCDSRequest):
    def __init__(self,
                 plot_ao_peaks=True, 
                 show=False, 
                 balligator_flag=False,
                 nb_bar_on_chart=300, 
                 min_bar_on_chart=299, 
                 balligator_period_jaws=89, cds_required_amount_of_bar_for_calc=None, nb_bar_to_retrieve=None, 
                 show_grid=False, 
                 subtitle_x_pos=0.07, subtitle_y_pos=0.9, subtitle_ha="left", subtitle_fontsize=10, title_x_pos=0.055, title_y_pos=0.96, title_ha="left", title_fontsize=14, jaw_line_width=1, teeth_line_width=1, lips_line_width=1, fig_ratio_x=24, fig_ratio_y=14, fdb_marker_size=7, fractal_marker_size=6, ac_signals_marker_size=32, saucer_marker_size=16, fractal_degreehigher_marker_size=20, price_peak_marker_size=36, ao_peaks_marker_size=42, fdb_signal_marker="o", fractal_up_marker="^", fractal_up_marker_higher="^", fractal_dn_marker_higher="v", fractal_dn_marker="v", ac_signal_marker="o", acb_plot_type="scatter", ao_peak_above_marker_higher="^", ao_peak_bellow__marker_higher="v", saucer_marker="|", zcol_marker="|", aop_bellow_color="r", aop_above_color="g", ao_upbar_color="g", ao_dnbar_color="r", ac_up_color="darkgreen", ac_dn_color="darkred", fdb_signal_buy_color="g", fdb_signal_sell_color="r", jaw_color="blue", teeth_color="red", lips_color="green", fractal_up_color="blue", fractal_dn_color="blue", fractal_dn_color_higher="blue", fractal_up_color_higher="blue", ac_signal_buy_color="lightgreen", ac_signal_sell_color="yellow", saucer_buy_color="g", saucer_sell_color="r", price_peak_bellow_marker="o", price_peak_above_marker="o", price_peak_above_color="g", price_peak_bellow_color="r", ao_peak_offset_value=0, 
                 plot_style="yahoo", 
                 ao_plot_type="bar", 
                 ac_plot_type="bar", 
                 main_plot_panel_id=0, 
                 ao_plot_panel_id=1, 
                 ac_plot_panel_id=2,
                 *args, 
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.plot_ao_peaks = plot_ao_peaks
        self.show = show
        #self.big_alligator_flag = big_alligator_flag
        
        
        
        # IMPORTED from JGTChartConfig (Migrating from JGTChartConfig to JGTADSRequest)
        self.nb_bar_on_chart = nb_bar_on_chart
        self.min_bar_on_chart = min_bar_on_chart
        self.balligator_period_jaws = balligator_period_jaws if balligator_flag else 0 #balligator_period_jaws will be 0 if it is not used
        self.cds_required_amount_of_bar_for_calc = cds_required_amount_of_bar_for_calc if cds_required_amount_of_bar_for_calc is not None else self.balligator_period_jaws
        self.nb_bar_to_retrieve = nb_bar_to_retrieve if nb_bar_to_retrieve is not None else self.nb_bar_on_chart + self.cds_required_amount_of_bar_for_calc
        self.show_grid = show_grid
        self.subtitle_x_pos = subtitle_x_pos
        self.subtitle_y_pos = subtitle_y_pos
        self.subtitle_ha = subtitle_ha
        self.subtitle_fontsize = subtitle_fontsize
        self.title_x_pos = title_x_pos
        self.title_y_pos = title_y_pos
        self.title_ha = title_ha
        self.title_fontsize = title_fontsize
        self.jaw_line_width = jaw_line_width
        self.teeth_line_width = teeth_line_width
        self.lips_line_width = lips_line_width
        self.fig_ratio_x = fig_ratio_x
        self.fig_ratio_y = fig_ratio_y
        self.fdb_marker_size = fdb_marker_size
        self.fractal_marker_size = fractal_marker_size
        self.ac_signals_marker_size = ac_signals_marker_size
        self.saucer_marker_size = saucer_marker_size
        self.fractal_degreehigher_marker_size = fractal_degreehigher_marker_size
        self.price_peak_marker_size = price_peak_marker_size
        self.ao_peaks_marker_size = ao_peaks_marker_size
        self.fdb_signal_marker = fdb_signal_marker
        self.fractal_up_marker = fractal_up_marker
        self.fractal_up_marker_higher = fractal_up_marker_higher
        self.fractal_dn_marker_higher = fractal_dn_marker_higher
        self.fractal_dn_marker = fractal_dn_marker
        self.ac_signal_marker = ac_signal_marker
        self.acb_plot_type = acb_plot_type
        self.ao_peak_above_marker_higher = ao_peak_above_marker_higher
        self.ao_peak_bellow__marker_higher = ao_peak_bellow__marker_higher
        self.saucer_marker = saucer_marker
        self.zcol_marker = zcol_marker
        self.aop_bellow_color = aop_bellow_color
        self.aop_above_color = aop_above_color
        self.ao_upbar_color = ao_upbar_color
        self.ao_dnbar_color = ao_dnbar_color
        self.ac_up_color = ac_up_color
        self.ac_dn_color = ac_dn_color
        self.fdb_signal_buy_color = fdb_signal_buy_color
        self.fdb_signal_sell_color = fdb_signal_sell_color
        self.jaw_color = jaw_color
        self.teeth_color = teeth_color
        self.lips_color = lips_color
        self.fractal_up_color = fractal_up_color
        self.fractal_dn_color = fractal_dn_color
        self.fractal_dn_color_higher = fractal_dn_color_higher
        self.fractal_up_color_higher = fractal_up_color_higher
        self.ac_signal_buy_color = ac_signal_buy_color
        self.ac_signal_sell_color = ac_signal_sell_color
        self.saucer_buy_color = saucer_buy_color
        self.saucer_sell_color = saucer_sell_color
        self.price_peak_bellow_marker = price_peak_bellow_marker
        self.price_peak_above_marker = price_peak_above_marker
        self.price_peak_above_color = price_peak_above_color
        self.price_peak_bellow_color = price_peak_bellow_color
        self.ao_peak_offset_value = ao_peak_offset_value
        self.plot_style = plot_style
        self.ao_plot_type = ao_plot_type
        self.ac_plot_type = ac_plot_type
        self.main_plot_panel_id = main_plot_panel_id
        self.ao_plot_panel_id = ao_plot_panel_id
        self.ac_plot_panel_id = ac_plot_panel_id


# Create an instance with default values
default_config = JGTADSRequest()

        