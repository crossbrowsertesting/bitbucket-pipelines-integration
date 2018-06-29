# Bitbucket Pipline Integration

Bitbucket Pipelines is a CI service that allows automatic building, testing, and/or deployment of the code in your Bitbucket repository. It is also compatible with CrossBrowserTesting.

## Basic setup

1. Enable Pipelines in the settings for your repository
2. Add your CBT username and authkey as environment variables in the Pipelines settings of your repository (in this example, they are named CBT_USERNAME and CBT_AUTHKEY).
3. Create a file called "bitbucket-pipelines.yml." The contents/structure of this file will vary based on your CI process/setup, but generally you will want to follow this basic structure:
      - Install any dependencies needed for your application
      - Start a local connection to CBT
      - Run your tests
      - Close the local connection

In this example, we use the two shell scripts in the cbt_scripts folder to start and close a local connection. We encourage you to use these, as they are the easiest way to set up a local connection in a Pipeline build.
Since this is a working example for our Python script, we have also included a template bitbucket-pipelines.yml file that contains no extra steps and has commented spaces to place your code in. Fill in the commands needed to build and execute your tests, then place your bitbucket-pipelines.yml file and cbt_scripts folder in the root of your repository.
Once everything is set up, your bitbucket-pipelines.yml file will run after every commit (you can change the conditions that trigger a build in your Pipelines settings). A successful run will look something like this:
![Bitbucket Pipeline build](https://github.com/crossbrowsertesting/bitbucket-pipelines-integration/images/successful_build.png)


## Considerations

You will need to ensure that the local connection is closed after your tests are complete. In this example, the command to run the test is placed after the command "set +e." This makes it so that even if something happens during that test that throws an uncaught exception or ends execution prematurely, the next command still executes and closes the local connection. Otherwise, the build would exit upon errors and leave the local connection open. You can read more about set -e and set +e [here](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html). We recommend using the start_connection.sh and stop_connection.sh scripts along with the set +e command since this requires no alteration to your code, but the local connection can also be closed by making an API call to [retrieve the ID](https://crossbrowsertesting.com/apidocs/v3/tunnels.html#!/default/get_tunnels) and [stop the local connection](https://crossbrowsertesting.com/apidocs/v3/tunnels.html#!/default/delete_tunnels_tunnel_id). A third way to open/close tunnels is to use our nodeJS module. The NodeJS module and the API calls can be used within the error handling on your test scripts.

## Further Support
If you run into any trouble, you can contact our support team, reference [Atlassian's documentation](https://confluence.atlassian.com/bitbucket/build-test-and-deploy-with-pipelines-792496469.html), or take a look at our [help pages](https://help.crossbrowsertesting.com/local-connection/general/local-tunnel-overview/).