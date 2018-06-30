# Big Brother

## Big Brother is a Flask/Python backend webapp that exposes two APIs for tracking ad data and getting statistics on those ads.

### So what does it have?

There are 2 main endpoints:
1. /track [GET, POST]
2. /track/statistics [GET]

#### To POST a new tracking event, you need the following data in your request body
    
    "track_type": "HOVER" OR "CLICK" OR "SCROLL" OR "CLOSE" OR "IMPRESSION"
    "ad_format": "MOBILE" OR "DESKTOP" OR "APP_BROWSER" OR "OTHER" OR "TABLET" 
    "ad_name": "" <some unique name for the add you are tracking>
    "ip": "1.1.1.1" <the IP address from which the tracking event occured>

If your "track_type" is "HOVER" then the following two elements are also required:

    "x_pixel": <the x cooridnate where the HOVER occured>
    "y_pixel": <the y cooridnate where the HOVER occured>

#### To GET some tracking events, you need any subset of the following URL parameters passed to /track
Note: URL parameters are NOT surrounded by quote markers

    track_type 
        HOVER <a single type> 
        HOVER,CLICK,SCROLL <a comma seperated list of types>
        ALL (default if blank) <a special keyword meaning all available types>
    ad_name
        Viagra <a single ad> 
        Viagra, Cialis, Levitra <a comma seperated list of ads>
        ALL (default if blank) <a special keyword meaning all available ads>
    start_ip
        1.1.1.1 <a plain old IP address>
        0.0.0.0 (default if blank)
    end_ip
        192.168.1.1 <a plain old IP address>
        255.255.255.255 (default if blank)
    start_timestamp
        2018-06-30T04:30:02.527960+00:00 <a UTC time zoned formated date and time string>
        0000-00-00T--:00:00.000000+00:00 (default) this just means 'the begining of time'
    end_timestamp
        2018-06-30T04:30:02.527960+00:00 <a UTC time zoned formated date and time string>
        9999-99-99T--:99:99.999999+00:00 (default) this just means 'the begining of time'
    ad_format
        MOBILE <a single format> 
        DESKTOP,TABLET,APP_BROWSER <a comma seperated list of format>
        ALL (default if blank) <a special keyword meaning all available format>

#### To GET some statistics, send a request to /track/statistics

Here's the fun part.... you can use the exact same URL parameters from GET /track (above) to limit your statistics. This way, if you only want statistics about a certain IP range, or a specific ad, both, or any combination you can think of, just add the same URL parameters to /track/statistics, like:
    
    /track/statistics/ad_name=Cialis&start_ip=8.8.8.8&end_ip=9.9.9.9
    

To run the app, build the Docker image and deploy the container. It should expose the app on port 5000.
If you have trouble building the Docker image and/or running the resulting container, you can also run the app directly (assuming you have the dependencies installed) via

    sh visor/bootstrap.sh