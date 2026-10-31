# Import built-in Python modules for handling JSON data and making HTTP requests
import json
import urllib.request
import urllib.parse

# Import NiFi's native Python API framework components for data transformation
from nifiapi.flowfiletransform import FlowFileTransform, FlowFileTransformResult

# Define the custom processor class inheriting from NiFi's FlowFileTransform base class
class FetchSeeClickFix(FlowFileTransform):
    
    # Nested Java configuration block required by NiFi 2.x 
    # This maps the Python class to NiFi's underlying Java interface architecture
    class Java:
        implements = ['org.apache.nifi.python.processor.FlowFileTransform']

    def __init__(self, **kwargs):
        # Initialize the parent class constructor
        super().__init__(**kwargs)

    # Metadata displayed in the NiFi UI when you search for or configure the processor
    class ProcessorDetails:
        version = "1.0.0"
        description = "Fetches SeeClickFix issues and writes formatted JSON to FlowFile content."
        tags = ["api", "seeclickfix", "json", "python"]

    # The core execution method triggered whenever a FlowFile passes through this processor
    def transform(self, context, flowfile):
        try:
            # Step 1: Define query parameters for the API request
            params = {
                'place_url': 'bernalillo-county',
                'per_page': '100'
            }
            
            # Safely encode parameters into a URL query string (e.g., place_url=bernalillo-county&per_page=100)
            query_string = urllib.parse.urlencode(params)
            url = f'https://seeclickfix.com/api/v2/issues?{query_string}'

            # Step 2: Build the HTTP request object with a custom User-Agent header
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Apache-NiFi-Python-Processor'}
            )
            
            # Step 3: Execute the HTTP request and read the response data
            with urllib.request.urlopen(req) as response:
                raw_reply = response.read().decode('utf-8')  # Read bytes and decode to string
                reply = json.loads(raw_reply)                # Parse string into a Python dictionary

            # Step 4: Pretty-print the dictionary back into a nicely formatted JSON string (4-space indentation)
            formatted_data = json.dumps(reply, indent=4)

            # Step 5: Return a success result containing the new content and custom FlowFile attributes
            return FlowFileTransformResult(
                relationship="success",
                contents=formatted_data,
                attributes={"seeclickfix.fetch.status": "success"}
            )
            
        except Exception as e:
            # Error Handling: Catch network timeouts, connection drops, or parsing failures
            error_data = json.dumps({"error": str(e)}, indent=4)
            
            # Route the FlowFile to the 'failure' relationship with error details in the content and attributes
            return FlowFileTransformResult(
                relationship="failure",
                contents=error_data,
                attributes={"seeclickfix.fetch.status": "failed"}
            )