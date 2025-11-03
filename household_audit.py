import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def main():
    # Initialize data storage
    data = pd.DataFrame(columns=['date', 'category', 'item', 'weight_grams', 'notes'])
    categories = ['Food Packaging', 'Plastic Film', 'Food Scraps', 'Personal Care', 'Other Plastics', 'Other Paper/Cardboard', 'Miscellaneous']
    
    print("🏠 HOUSEHOLD WASTE AUDIT TOOL")
    print("Track your waste and get a personalized reduction plan!\n")
    
    while True:
        print("\nOptions:")
        print("1. Add waste entry")
        print("2. Show summary report")
        print("3. View charts")
        print("4. Generate action plan")
        print("5. Save data")
        print("6. Load data")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            print("\nAdding new waste entry:")
            print("Available Categories:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            date = input("Enter date (YYYY-MM-DD) or press enter for today: ").strip()
            if not date:
                date = datetime.now().strftime("%Y-%m-%d")
            
            try:
                cat_choice = int(input("Enter category number: ")) - 1
                category = categories[cat_choice]
            except (ValueError, IndexError):
                print("Invalid category selection.")
                continue
            
            item = input("Enter item description: ").strip()
            weight = input("Enter weight in grams: ").strip()
            
            try:
                weight_grams = float(weight)
            except ValueError:
                print("Invalid weight. Please enter a number.")
                continue
            
            notes = input("Enter any notes (optional): ").strip()
            
            new_entry = {
                'date': date,
                'category': category,
                'item': item,
                'weight_grams': weight_grams,
                'notes': notes
            }
            data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
            print(f"✓ Added: {weight_grams}g of {item} ({category})")
        
        elif choice == '2':
            if data.empty:
                print("No data available. Please add some waste entries first.")
                continue
            
            print("\n" + "="*50)
            print("WASTE AUDIT SUMMARY REPORT")
            print("="*50)
            
            total_waste = data['weight_grams'].sum()
            print(f"Total Waste: {total_waste:,} grams ({total_waste/1000:.2f} kg)")
            
            print("\n--- Waste by Category ---")
            category_totals = data.groupby('category')['weight_grams'].sum().sort_values(ascending=False)
            for category, weight in category_totals.items():
                percentage = (weight / total_waste) * 100
                print(f"{category}: {weight:,}g ({percentage:.1f}%)")
            
            days = data['date'].nunique()
            daily_avg = total_waste / days if days > 0 else 0
            print(f"\nDaily Average: {daily_avg:,.0f} grams")
            print(f"Data collected over {days} days")
        
        elif choice == '3':
            if data.empty:
                print("No data available for visualization.")
                continue
            
            # Create simple charts without seaborn
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Pie chart
            category_totals = data.groupby('category')['weight_grams'].sum()
            ax1.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%', startangle=90)
            ax1.set_title('Waste Composition by Category')
            
            # Bar chart
            daily_totals = data.groupby('date')['weight_grams'].sum()
            ax2.bar(range(len(daily_totals)), daily_totals.values, color='skyblue', alpha=0.7)
            ax2.set_title('Daily Waste Generation')
            ax2.set_xlabel('Days')
            ax2.set_ylabel('Weight (grams)')
            ax2.set_xticks(range(len(daily_totals)))
            ax2.set_xticklabels([str(i+1) for i in range(len(daily_totals))])
            
            plt.tight_layout()
            plt.show()
        
        elif choice == '4':
            if data.empty:
                print("No data available to generate action plan.")
                continue
            
            category_totals = data.groupby('category')['weight_grams'].sum().sort_values(ascending=False)
            top_categories = category_totals.head(3)
            
            print("\n" + "="*50)
            print("PERSONALIZED WASTE REDUCTION ACTION PLAN")
            print("="*50)
            
            action_strategies = {
                'Food Packaging': [
                    "• Buy in bulk using reusable containers",
                    "• Choose products with minimal/recyclable packaging",
                    "• Use reusable bags for grocery shopping"
                ],
                'Plastic Film': [
                    "• Switch to reusable silicone bags",
                    "• Use beeswax wraps instead of plastic wrap",
                    "• Choose loose produce instead of pre-packaged"
                ],
                'Food Scraps': [
                    "• Start composting kitchen scraps",
                    "• Plan meals to reduce food waste",
                    "• Use vegetable scraps for homemade broth"
                ],
                'Personal Care': [
                    "• Switch to bamboo toothbrushes",
                    "• Use shampoo and conditioner bars",
                    "• Choose safety razors instead of disposable"
                ],
                'Other Plastics': [
                    "• Carry a reusable water bottle and coffee cup",
                    "• Use reusable straws and utensils",
                    "• Choose glass or metal containers over plastic"
                ],
                'Other Paper/Cardboard': [
                    "• Reuse cardboard boxes for storage",
                    "• Use both sides of paper before recycling",
                    "• Switch to digital bills and statements"
                ]
            }
            
            for category in top_categories.index:
                if category in action_strategies:
                    print(f"\n🎯 For {category} ({top_categories[category]:,}g):")
                    for action in action_strategies[category]:
                        print(f"  {action}")
            
            print(f"\n💡 Additional Tips:")
            print("  • Conduct regular audits to track progress")
            print("  • Set reduction goals and celebrate achievements")
            print("  • Involve all household members in waste reduction")
        
        elif choice == '5':
            if data.empty:
                print("No data to save.")
                continue
            filename = input("Enter filename (or press enter for 'waste_data.csv'): ").strip()
            if not filename:
                filename = "waste_data.csv"
            data.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        
        elif choice == '6':
            filename = input("Enter filename to load (or press enter for 'waste_data.csv'): ").strip()
            if not filename:
                filename = "waste_data.csv"
            if os.path.exists(filename):
                data = pd.read_csv(filename)
                print(f"Data loaded from {filename}")
            else:
                print(f"File {filename} not found.")
        
        elif choice == '7':
            print("Thank you for using the Household Waste Audit Tool!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()