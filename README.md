# Jamie

## Installing Modules
pip install -r requirements.txt

## Make .env file add google api key there as such:
GOOGLE_API_KEY=your_key_here_no_quotes
#to get dkey sign up to deepgram with github or email (gmail doesn't work gives errors) # and click create api key button once logged in
DEEPGRAM_API_KEY=deepgram-api-key-no-quotes 
OPEN_AI_KEY=sk-your-open-ai-key
AIRTABLE_ACCESS_TOKEN=patjS41bOtLK5Fwwz.7433922cf15958a36e71e38209223484717af05a0fa617bef73de8d7a28f8d60

## You can now run code like so
In the root directory of the project run following code in terminal
streamlit run .\streamlit_app.py

This command will keep running , you may need to run it multiple times, if it just executes and you can type new command it didn't work, try like 10 - 20 times it will keep running eventually.