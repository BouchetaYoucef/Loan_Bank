web: sh setup.sh && streamlit run app.py
web: rake db:migrate && bin/rails server -b 0.0.0.0 -p ${PORT:-3000} && bin/rails tailwindcss:watch