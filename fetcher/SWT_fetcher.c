/*****************************************************************************
 *                                  _   _ ____  _
 *  Project                     ___| | | |  _ \| |
 *                             / __| | | | |_) | |
 *                            | (__| |_| |  _ <| |___
 *                             \___|\___/|_| \_\_____|
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include <curl/curl.h>
//#include <curl/types.h>
#include <curl/easy.h>

static size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream)
{
  int written = fwrite(ptr, size, nmemb, (FILE *)stream);
  return written;
}

int main(int argc, char* argv[])
{
  CURL *curl_handle;
  static const char *headerfilename = "./cookie.txt";
  FILE *headerfile;
  FILE *bodyfile;

  static const char *second_url = "http://www.buytickets.southwesttrains.co.uk/"
  "CheaperSlowerTrains.aspx?Command=FindCheaperTrains";

  char first_url[512];
  char data_file_name[20];

  if (argc != 3) {
  	perror("Usage: fetch_stations_pricelist ST1 ST2");
	exit(1);
  }
  for (int i = 1; i<3; i++) {
  	if (strlen(argv[i]) != 3) {
		perror("station codes should be 3 char long\n");
		exit(1);
	}
  }

  snprintf(&first_url, 512,
  "https://www.buytickets.southwesttrains.co.uk/DataPassedIn.aspx?"
  	"ori=%s+&dest=%s+&outDate=19%%2f08%%2f2014&outHourField=11&"
	"outMinuteField=30&noa=1&noc=0&rcCode=YNG&rcNum=1", argv[1], argv[2]);
  snprintf(&data_file_name, 20, "%s/%s_%s.html", argv[1], argv[1], argv[2]);
  curl_global_init(CURL_GLOBAL_ALL);

  /* init the curl session */
  curl_handle = curl_easy_init();

  /* set URL to get */
  curl_easy_setopt(curl_handle,
  CURLOPT_URL, first_url);
  /* no progress meter please */
  curl_easy_setopt(curl_handle, CURLOPT_NOPROGRESS, 1L);
  //curl_easy_setopt(curl_handle, CURLOPT_COOKIEFILE, "cookie.txt");

  /* send all data to this function  */
  curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, write_data);

  /* open the files */
  headerfile = fopen(headerfilename,"w");
  if (headerfile == NULL) {
    curl_easy_cleanup(curl_handle);
    return -1;
  }
  bodyfile = fopen(data_file_name,"w");
  if (bodyfile == NULL) {
    curl_easy_cleanup(curl_handle);
    return -1;
  }

  /* we want the headers to this file handle */
  curl_easy_setopt(curl_handle,   CURLOPT_WRITEHEADER, headerfile);
//  curl_easy_setopr(curl_handle,   CURLOPT_WRITEDATA, );

  /*
   * Notice here that if you want the actual data sent anywhere else but
   * stdout, you should consider using the CURLOPT_WRITEDATA option.  */

  /* get cookies! */
  curl_easy_perform(curl_handle);

  fclose(headerfile);
  /* Part II. Get actual data */
  curl_easy_setopt(curl_handle,   CURLOPT_WRITEHEADER, NULL);
  curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, bodyfile);
  curl_easy_setopt(curl_handle, CURLOPT_COOKIEFILE, headerfilename);
  curl_easy_setopt(curl_handle, CURLOPT_URL, second_url);
  curl_easy_perform(curl_handle);

  /* close the header file */
  fclose(bodyfile);

  /* cleanup curl stuff */
  curl_easy_cleanup(curl_handle);

  return 0;
}
