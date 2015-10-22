filepicker.setKey("AlJgw2qgSsaTuk2G8CLAqz");

function upload() {
	filepicker.pick(
	function(Blob){
 	   console.log(Blob.url);
 	}
  );
}