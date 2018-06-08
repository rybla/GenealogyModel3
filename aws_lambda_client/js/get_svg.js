AWS.config.region = 'us-west-2'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-west-2:f6649357-417f-443c-8a4f-c853855d44ad',
});
function get_svg(result){
    console.log(result)
    var pullParams = {
      FunctionName : 'geneology_lambda_function',
      InvocationType : 'RequestResponse',
      LogType : 'None',
      Payload: JSON.stringify(result),
    };
    var lambda = new AWS.Lambda({region: 'us-west-2', apiVersion: '2015-03-31'});
    lambda.invoke(pullParams, function(error, data) {
      if (error) {
          place_text_on_svg("Server Error")
        prompt(error);
      } else {
        data = JSON.parse(data.Payload);
        if (data.success){
            html_code = JSON.parse(data.success);
            //console.log(html_code)
            $("#downloadbutton").show()
            document.getElementById("svg_item").innerHTML = html_code;
        }
      }
  });
}
