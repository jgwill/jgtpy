import argparse

def main():
    parser = argparse.ArgumentParser(description="Mouth Water Plotter CLI")
    parser.add_argument("--show", action="store_true", default=False, help="Display the chart")
    parser.add_argument("--save", type=str, help="Save chart to file (e.g., output.png)")
    parser.add_argument("-mw", "--mouth_water_flag", action="store_true", 
                       help="Force mouth water analysis")

    args = parser.parse_args()

    # Create plotter and generate chart
    plotter = MouthWaterPlotter()
    fig, axes = plotter.create_specialized_mouth_water_chart(
        data, args.instrument, args.timeframe, args.chart_type, args.show
    )
    
    # Save chart if requested
    if hasattr(args, 'save') and args.save:
        fig.savefig(args.save, dpi=150, bbox_inches='tight')
        print(f"Chart saved to: {args.save}")

if __name__ == "__main__":
    main() 