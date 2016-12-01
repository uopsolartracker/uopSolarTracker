#include "stdio.h"
#include "opencv/highgui.h"
#include "ASICamera2.h"
#include <time.h>
#include <unistd.h>
#include <sys/time.h>
#include <string.h>
#include <stdlib.h>

#define KNRM  "\x1B[0m"
#define KRED  "\x1B[31m"
#define KGRN  "\x1B[32m"
#define KYEL  "\x1B[33m"
#define KBLU  "\x1B[34m"
#define KMAG  "\x1B[35m"
#define KCYN  "\x1B[36m"
#define KWHT  "\x1B[37m"


static unsigned long GetTickCount()
{
#ifdef _MAC
    struct timeval  now;
    gettimeofday(&now, NULL);
    unsigned long ul_ms = now.tv_usec/1000 + now.tv_sec*1000;
    return ul_ms;
#else
   struct timespec ts;
   clock_gettime(CLOCK_MONOTONIC,&ts);
   return (ts.tv_sec*1000 + ts.tv_nsec/(1000*1000));
#endif
}

char* getTime(){
	static int seconds_last = 99;
	char TimeString[128];
	timeval curTime;
	gettimeofday(&curTime, NULL);
	if (seconds_last == curTime.tv_sec)
    return 0;

	seconds_last = curTime.tv_sec;
	strftime(TimeString, 80, "%Y%m%d %H:%M:%S", localtime(&curTime.tv_sec));
    return TimeString;
}


int main (int argc, char * argv[])
{

int time1,time2,timeSave;
int count=0;

int bMain=1;
char buf[1024]={0};

std::string fileName ="IMAGE.PNG";

int width=1080;
int height=940;
int bin=1;
int Image_type=0;
int asiGain=50;
int asiBandwidth=40;
int asiExposure=2;
int asiWBR=50;
int asiWBB=50;
int asiGamma=50;
int asiBrightness=50;

char optChar[10];

IplImage *pRgb;

char const* bayer[] = {"RG","BG","GR","GB"};
int CamNum=0;
int i;

printf("\n%sUsage:\n", KRED);
printf(" ./startCapture -w 640 -h 480 -e 50000 -g 50 -t 1 -b 1 -f Timelapse.PNG\n\n");
printf("%sSwitches: \n",KYEL);
printf(" -w = Width	 - Default = Camera Max Width \n");
printf(" -h = Height	 - Default = Camera Max Height \n");
printf(" -e = Exposure	 - Default = 50000ns \n");
printf(" -g = Gain	 - Default = 50 \n");
printf(" -a = Gamma	 - Default = 50 \n");
printf(" -r = Brightness - Default = 50 \n");
printf(" -x = WB_Red     - Default = 50  - White Balance Red \n");
printf(" -y = WB_Blue    - Default = 50  - White Balance Blue \n");
printf(" -b = Bin        - Default = 1   - 1 = binning OFF, 2 = 2x2 binning \n");
printf(" -t = Image Type - Default = 0   - 0 = RAW8, 1 = RAW16, 2 = RGB24 \n");
printf(" -s = USB Speed  - Default = 40  - Values between 40-100, This is BandwidthOverload \n");
printf(" -f = Filename   - Default = IMAGE.PNG \n\n");
printf("%s", KNRM);
printf("We're about to check for args\n");
 int opt;
  while ((opt = getopt (argc, argv, "w:h:e:g:a:r:x:y:b:t:s:f:")) != -1)
  {
    switch (opt)
    {
      	case 'w':
	width=atoi(optarg);
//	printf("./startCapture width: %d ", width);
	  break;
	case 'h':
	height=atoi(optarg);
//	printf("height: %d ", height);
	  break;
 	case 'e':
        asiExposure=atoi(optarg);
//        printf("exposure: %d ", asiExposure);
          break;
	case 'g':
        asiGain=atoi(optarg);
//        printf("gain: %d ", asiGain);
          break;
        case 'a':
        asiGamma=atoi(optarg);
//        printf("gamma: %d ", asiGamma);
          break;
        case 'r':
        asiBrightness=atoi(optarg);
//        printf("brightness: %d ", asiBrightness);
          break;
        case 'x':
        asiWBR=atoi(optarg);
//        printf("wbr: %d ", asiWBR);
          break;
        case 'y':
        asiWBB=atoi(optarg);
//        printf("wbb: %d ", asiWBB);
          break;
	case 'b':
        bin=atoi(optarg);
//        printf("bin: %d ", bin);
          break;
	case 't':
        Image_type=atoi(optarg);
//        printf("type: %d ", Image_type);
          break;
	case 's':
        asiBandwidth=atoi(optarg);
//        printf("usbspeed: %d\n", asiBandwidth);
          break;
	case 'f':
        fileName=(optarg);
          break;
    }
  }



printf("We're about to check for number of devices\n");
int numDevices = ASIGetNumOfConnectedCameras();
printf("We just checked for number of devices\n");
    if(numDevices <= 0)
    	{
	printf("\nNo Connected Camera...\n");
	width=1;	//Set to 1 when NO Cameras are connected to avoid error: OpenCV Error: Insufficient memory
	height=1;	//Set to 1 when NO Cameras are connected to avoid error: OpenCV Error: Insufficient memory
	}
    else
	printf("\nListing Attached Cameras:\n");

ASI_CAMERA_INFO ASICameraInfo;
    for(i = 0; i < numDevices; i++)
    {
	ASIGetCameraProperty(&ASICameraInfo, i);
	printf("CameraID: %d %s\n",i, ASICameraInfo.Name);
    }

if(ASIOpenCamera(CamNum) != ASI_SUCCESS)
	{
		printf("Open Camera ERROR, Check that you have root permissions!\n");
	}

	printf("\n%s Information:\n",ASICameraInfo.Name);
	int iMaxWidth, iMaxHeight;
	iMaxWidth = ASICameraInfo.MaxWidth;
	iMaxHeight =  ASICameraInfo.MaxHeight;
	printf("Resolution:%dx%d\n", iMaxWidth, iMaxHeight);
	if(ASICameraInfo.IsColorCam)
		printf("Color Camera: bayer pattern:%s\n",bayer[ASICameraInfo.BayerPattern]);
	else
		printf("Mono camera\n");


ASI_CONTROL_CAPS ControlCaps;
	int iNumOfCtrl = 0;
	ASIGetNumOfControls(CamNum, &iNumOfCtrl);

	for( i = 0; i < iNumOfCtrl; i++)
	{
		ASIGetControlCaps(CamNum, i, &ControlCaps);
		printf("%s\n", ControlCaps.Name);
	}

	if(width == 0 || height == 0)
	{
		width = iMaxWidth;
		height = iMaxHeight;
	}

	long ltemp = 0;
	ASI_BOOL bAuto = ASI_FALSE;
	ASIGetControlValue(CamNum, ASI_TEMPERATURE, &ltemp, &bAuto);
	printf("sensor temperature:%02f\n", (float)ltemp/10.0);

printf("%s",KGRN);
	printf("\nCapture Settings: \n");
	printf(" Resolution: %dx%d \n",width,height);
	printf(" Exposure: %d\n",asiExposure);
	printf(" Brightness: %d\n",asiBrightness);
	printf(" Gain: %d\n",asiGain);
	printf(" Gamma: %d\n",asiGamma);
	printf(" WB Red: %d\n",asiWBR);
	printf(" WB Blue: %d\n",asiWBB);
	printf(" Binning: %d\n",bin);
	printf(" Image Type: %d\n",Image_type);
	printf(" USB Speed: %d\n",asiBandwidth);
printf("%s",KNRM);

	//ASIGetROIFormat(CamNum, &width, &height, &bin, (ASI_IMG_TYPE*)&Image_type);
	if(Image_type == 1)//ASI_IMG_RAW16
		{
		printf("\n\nASI_IMG_RAW16\n\n");
		pRgb=cvCreateImage(cvSize(width, height), IPL_DEPTH_16U, 1);
		}
	else if(Image_type == 2)//ASI_IMGRGB24
		{
		printf("\n\nASI_IMG_RGB24\n\n");
		pRgb=cvCreateImage(cvSize(width, height), IPL_DEPTH_8U, 3);
		}
	else	{
		printf("\n\nASI_IMG_RAW8\n\n");
		pRgb=cvCreateImage(cvSize(width, height), IPL_DEPTH_8U, 1);
		}
	//long imgSize = width*height*(1 + (Image_type==ASI_IMG_RAW16));
	//long displaySize = width*height*(1 + (Image_type==ASI_IMG_RAW16));
	//unsigned char* imgBuf = new unsigned char[imgSize];
//	pRgb=cvCreateImage(cvSize(width, height), IPL_DEPTH_8U, 3);

	ASISetControlValue(CamNum, ASI_TEMPERATURE, 50*1000, ASI_FALSE);
	ASISetControlValue(CamNum, ASI_GAIN, asiGain, ASI_FALSE);
	ASISetControlValue(CamNum, ASI_BANDWIDTHOVERLOAD, asiBandwidth, ASI_FALSE);
	ASISetControlValue(CamNum, ASI_EXPOSURE, asiExposure, ASI_FALSE);
	ASISetControlValue(CamNum, ASI_WB_R, asiWBR, ASI_FALSE);
	ASISetControlValue(CamNum, ASI_WB_B, asiWBB, ASI_FALSE);

	time1 = GetTickCount();
	timeSave = GetTickCount();

	ASI_EXPOSURE_STATUS status;
	int iDropped = 0;
	while(bMain)
	{
		ASIStartExposure(CamNum, ASI_FALSE);
		usleep(10000);//10ms
		status = ASI_EXP_WORKING;
		while(status == ASI_EXP_WORKING)
		{
			ASIGetExpStatus(CamNum, &status);
		}


		if(status == ASI_EXP_SUCCESS)
		{

/*			ASIGetDataAfterExp(CamNum, imgBuf, imgSize);
			if(Image_type==ASI_IMG_RAW16)
			{
				unsigned short *pCv16bit = (unsigned short *)(pRgb->imageData);
				unsigned short *pImg16bit = (unsigned short *)imgBuf;
				for(int y = 0; y < height; y++)
				{
					memcpy(pCv16bit, pImg16bit, width*2);
					pCv16bit+=width;
					pImg16bit+=width;
				}
			}
			else{
				unsigned char *pCv8bit = (unsigned char *)pRgb->imageData;
				unsigned char *pImg8bit = (unsigned char *)imgBuf;
				for(int y = 0; y < height; y++)
				{
					memcpy(pCv8bit, pImg8bit, width);
					pCv8bit+=width;
					pImg8bit+=width;
				}
			}
*/
		ASIGetDataAfterExp(CamNum, (unsigned char*)pRgb->imageData, pRgb->imageSize);

		}

		time2 = GetTickCount();
		count++;
		if(time2-time1 > 1000 )
		{
			ASIGetDroppedFrames(CamNum, &iDropped);
			sprintf(buf, "fps:%d dropped frames:%lu ImageType:%d",count, iDropped, Image_type);
			sprintf(buf, "%s", getTime());
			count = 0;
			time1=GetTickCount();
			printf(buf);
			printf(".");
			printf("\n");
		}
		if (time2 - timeSave > 5000)
		  {
			cvSaveImage( fileName.c_str(), pRgb );
			timeSave = GetTickCount();
		  }
		if(Image_type != ASI_IMG_RGB24 && Image_type != ASI_IMG_RAW16)
		{
			cvSet(pRgb, CV_RGB(180, 180, 180));
			cvResetImageROI(pRgb);
		}
	}
END:

	ASIStopExposure(CamNum);
	ASICloseCamera(CamNum);
	cvReleaseImage(&pRgb);
	//if(imgBuf)
		//delete[] imgBuf;
	printf("main function over\n");


return 0;
}
