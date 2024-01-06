# SANDMAN: Sandbox Multi-Agent Network

## OpenAI API Key Instructions

Once you have the API key (message Lewis) then you need to update your system environment variables.

1. Windows > Edit the system environment variables
2. Click 'Environment Variables...'
3. In the 'System variables' box click 'New...'
4. Set Variable name as: OPENAI_API_KEY
5. Set Variable value as: <INSERT API KEY HERE>
6. You need to restart your IDE to fetch it using os.getenv when prompting
7. Test it works by running TextGenTest.py
