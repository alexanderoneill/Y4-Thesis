window.onload = init;

			function init() {
				
				// Get div that stores image, and the image itself
				var imageBox = document.getElementById("imageframe");
				var sourceImage = document.getElementById("sourceimage");

				// If the user has the cookie given by this site
				if (document.cookie.indexOf("IID") >= 0) {

					// Show div containing image, change image to processed image submitted
					// by user
					imageBox.style.display = "block";
					sourceImage.src = "static/faces/processed_images/".concat(getCookie("IID"))
					}
					else {
					
					// Keep image div hidden
					imageBox.style.display = "none";
				
				}

			
			}

			// v----------v CODE ADAPTED FROM W3SCHOOLS.COM v----------v
			function getCookie(c_name) {
				
				if (document.cookie.length > 0) {
					
					c_start = document.cookie.indexOf(c_name + "=");
					
					if (c_start != -1) {
						
						c_start = c_start + c_name.length + 1;
						c_end = document.cookie.indexOf(";", c_start);
						
						if (c_end == -1) {
							
							c_end = document.cookie.length;
						
						}
						
						return unescape(document.cookie.substring(c_start, c_end));
					
					}
				
				}
	
				return "";

			}
			// ^----------^ CODE ADAPTED FROM W3SCHOOLS.COM ^----------^