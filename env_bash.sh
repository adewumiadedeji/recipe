# Create template for team
cp .env .env.example
sed -i 's/=.*/=/' .env.example  # Remove values