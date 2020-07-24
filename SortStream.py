B
    �/_��  �               @   sX  d Z ddlZyddlZW n( ek
r@   e�d� e�d� Y nX yddlZW n( ek
rv   e�d� e�d� Y nX yddlZW n( ek
r�   e�d� e�d� Y nX yddlZW n( ek
r�   e�d	� e�d
� Y nX yddl	Z	W n* ek
�r   e�d� e�d� Y nX yddl
Z
W n* ek
�rR   e�d� e�d� Y nX yddlZW n* ek
�r�   e�d� e�d� Y nX ddlZddlZddlZdcdd�ZddlZddlZddlmZ ddlZddlZddlZddlZdddd�Zdedd�Zdfdd�Zdgd d!�Zdhd#d$�Zdid&d'�Zdjd(d)�Zd*d+� ZddlZddlZdd,lmZ d-d.� Z dkd0d1�Z!dd2l"m#Z# dd3l$m%Z% dd4l&m'Z' ddlZdd5lm(Z( ddlZdld9d:�Z)dmd=d>�Z*dnd?d@�Z+ddAl	m,Z, dBdC� Z-ddlZdodDdE�Z.dFgdfdGdH�Z/ddIl
m0Z0 ddJl1m2Z2 ddl3Z3dKdL� Z4dpdMdN�Z5ddlZddlZddl6Z6ddlZ7dd,lmZ ddlZdOdP� Z8dQd.� Z dRdS� Z9dTdU� Z:G dVdW� dWe7j;�Z<G dXdY� dYe7j;�Z=e>e7j?� e9� Z@dZZAee@deAd[�ZBeB�re7�C� ZDeD�Ed\� eD�Fd]� eD�Gd^d_� e<eDd`�ZHeH�I�  eH�J�  nDe7�C� ZDeD�Ed\� eD�Fda� eD�Gd^d_� e=eDeAdb�ZHeH�I�  eH�J�  dS )qzgGrant Holtes 2020
check of requiredPackages are installed, and if no calls Pip to install the packages
�    Nzpip install numpyzpip3 install numpyzpip install tkinterzpip3 install tkinterzpip install requestszpip3 install requestszpip install sklearnzpip3 install sklearnzpip install PyPDF2zpip3 install PyPDF2zpip install nltkzpip3 install nltkz"pip install pkg_resources.py2_warnz#pip3 install pkg_resources.py2_warnT�dataset�.�   �d   c          	   C   s$  d}d}t �t j�|��}d|krNt �t j�|d�� d}d}t|� ||fS t �t j�|d��}g }	x0|D ](}
d|
ks�|
dks�|
dkr�ql|	�|
� qlW td	�|	�� |	g kr�d
}d}t|� ||fS t|	�dkr�d}d}t|� ||fS ddgg}t	�  x�|	D ]�}t �t j�|d|��}t
�|� d}xv|D ]n}d}|d7 }|dd � dk�r|d}t j�|d||�}t|�}| �r|t|�}|�r.||k�r.|�||g� �q.W ||k �r d�|�}t|� d}�q W t
�|� tt j�||d �ddd��*}t�|�}x|D ]}|�|� �q�W W d Q R X ||fS )N� T�dataz6No 'data' folder found,
 please use the folder createdFr   �env�__pycache__zData folders found: {0}zMNo subfolders found in data,
 please add training data in folders by category�   zJOnly 1 category subfolder found in data,
 please add at least 2 categories�CategoryZTextr   �����z.pdfz-Please add at least {0} examples per categoryz.csv�w)�newline)�os�listdir�path�join�mkdir�print�append�format�len�setupTextPreProcess�randomZshuffle�pdf2txt�preprocessText�open�csv�writer�writerow)�
preprocess�filename�appPathZminPerClassZmaxPerClass�status�successfulBuildDataset�dirs�homeZ
catFolders�itemZdataList�categoryZ	dataPaths�cntr   Z	validFileZ
pathToData�text�csvfiler   �row� r-   �SortStreamRAW.py�buildDatasetB   sj    










r/   )�sha256�sortstream.licencec             C   sb   yHt �ttj�| |�d��}|d }t�� }t||�}||krBdS dS W n t	k
r\   dS X dS )z[
	Grant Holtes 26/6/20
	Check if a licence file is valid for the machine it is running on
	�rb�ZTFN)
�pickle�loadr   r   r   r   �uuid�getnode�getHash�FileNotFoundError)r"   �licenceFilename�XZlicenceDataZZlic�UUIDZZnewr-   r-   r.   �AuthenticateLicence�   s    
r=   c             C   s&   | | }t �t |��}t|��� }|S )N)�str�encoder0   Z	hexdigest)r<   r;   ZProductZByteProdr3   r-   r-   r.   r8   �   s    r8   c             C   s�   yt | �}W n tk
r(   d}d|fS X tt| ��dkrFd}d|fS t�� }t| �}|d }|d }d}t |�dkr�d}t| |d� d	}nt |�t |�kr�d}d	}nd
}||fS )Nz:Please enter a 12 digit numeric product key without spacesF�   r<   �email�����T)r<   zFProduct Key accepted, licence file created. Please restart applicationz&This Product Key has already been used)�int�
ValueErrorr   r>   r6   r7   �readDynamoDBAPI�UpdateDynamoDBAPI)�
productKeyZproductKeyInt�returnMessager<   ZDynamoDBCallZDB_UUIDZDB_email�validProductKeyr-   r-   r.   �checkProductKey�   s,    
rJ   c          	   C   sV   t �� }t||�}i }||d< ||d< ttj�|| �d��}t�||� W dQ R X dS )z�Grant Holtes
	Generate a licence file with format:
	{
		Z: The hash of UUID, X
		Key: The product key used to generate the licence
	}
	r3   �Key�wbN)	r6   r7   r8   r   r   r   r   r4   �dump)r:   r;   rG   r"   r<   r3   Zlicence�
pickleFiler-   r-   r.   �writeLicenceFile�   s    
rO   �Rhttps://r9uxgotjjc.execute-api.eu-west-1.amazonaws.com/default/lambda-microservicec             C   s�   ddddt | �iid�}tj||d�}|�� }y4|d }i }|d |d< |d |d< |d	 |d
< W n0 tk
r�   i }| |d< d|d< d|d
< Y nX |S )a  accepts a productKey, apiEndPoint
	returns all info about the unique row in the DB for the given product code in a dict.
	keys: "productkey", "email", "uuid_"
	if productKey doesnt exist in the DB, returns {ProductKey: productkey, email: None, UUID: None}
	�read�DocumentClassificationLicencerK   �
productkey)�	operation�	tableName�payload)�url�json�ItemrA   �uuid_r<   N)r>   �requests�getrX   �KeyError)�
ProductKey�apiEndPoint�Params�getReq�responseZproductInfoZ
returnDictr-   r-   r.   rE   �   s$    rE   rB   c             C   s|   dddt | �iddt |�idd�d�}tj||d	�}y0|�� }|d
 d }t|�t|�kr^dS dS W n   td� dS dS )z�accepts a productKey, UUID, apiEndPoint
	Updates the unique row in the DB with a new uuid_ value as given by the UUID input.
	returns a success status (True = successful update, False = failed update)
	�updaterR   rS   zset uuid_ = :uz:uZUPDATED_NEW)rK   ZUpdateExpressionZExpressionAttributeValuesZReturnValues)rT   rU   rV   )rW   rX   Z
AttributesrZ   TFz"error in updating dynomoDB requestN)r>   r[   r\   rX   rC   r   )r^   r<   r_   r`   ra   rb   ZnewUUIDr-   r-   r.   rF     s     	

rF   c             C   sB   dddt | �|t |�d�id�}ytj||d� dS    dS d	S )
z�accepts a productKey, email, uuid, apiEndPoint
	Creates a new item in the DB with the productKey, email, uuid provided. useful for enrolling new product keys.
	returns True if successful.
	ZcreaterR   rY   )rS   rA   rZ   )rT   rU   rV   )rW   rX   TFN)r>   r[   r\   )r^   rA   r<   r_   r`   r-   r-   r.   �createDynamoDBAPI4  s    rd   c             C   s$   d}| dd� � � dkr t| �}|S )zZ
	Grant Holtes 24/11/20
	uses premade functions and file exctension to load file as text
	r   r   Nz.pdf)�lowerr   )r   r*   r-   r-   r.   �loadFileU  s    rf   )�datetimec               C   s   t �� �d�S )Nz%Y%m%d_%H-%M-%S)rg   �now�strftimer-   r-   r-   r.   �YYYYMMDDHMSj  s    rj   �logsc          
   C   s�   t �|�}||kr&t �t j�||�� |dt�  d 7 }tt j�|||�ddd��D}t�|�}x| D ]}|�	|� qdW t
d�|t j�|||��� W d Q R X d S )N�_z.csvr   r   )r   zlogfile {0} saved at {1})r   r   r   r   r   rj   r   r   r   r   r   r   )�arrayr!   r"   ZsaveLocr&   r+   r   r,   r-   r-   r.   �saveLogsm  s    


rn   )�TfidfVectorizer)�OneHotEncoder)�LogisticRegression)�ndarray�model��  �
   c	          	   C   s�   t dddddd�}	|	�| ��� }
|
jd }tdd	d
d�}|�|
|�� d � ttj	�
||d�d��}t�|	|� W dQ R X ttj	�
||d�d��}t�||� W dQ R X dS )a$  
    Grant Holtes, 15/02/2020
    input:  xTrain, xTest; input training and test data, as preprocessed text in a list of strings,
            yTrain, yTest; target training and test data, as a finite set of text or numeric labels in a list.
    output: 3 sklearn models are saved to disk
    �asciiZwordg      �?g        i�  )Zstrip_accentsZanalyzerZmax_dfZmin_dfZmax_featuresr
   ZlbfgsZmultinomiali�  )ZsolverZmulti_classZmax_iterr   �vectorizerXrL   N�logisticT)ro   Zfit_transform�toarray�shaperq   ZfitZ	transposer   r   r   r   r4   rM   )ZxTrainZyTrainZxTestZyTest�saveloc�maxFeatures�	batchSize�epochsTrainr"   �
vectorizerZxTrainVectorisedZfeaturesCountrs   rN   r-   r-   r.   �createAndTrainModel�  s     
r�   rw   rx   c             C   s<   t �ttj�| |�d��}t �ttj�| |�d��}||fS )z�
    Grant Holtes, 15/02/2020
    input: locations of the 2 sklearn models and 1 tf model are saved to disk that are created when createAndTrainModel() is run
    output: a tuple of the loaded models

    Requires createAndTrainModel() has been run
    r2   )r4   r5   r   r   r   r   )�folderrw   rs   r"   r   ZModelr-   r-   r.   �	loadModel�  s    r�   c       
      C   s�   |\}}|rrt �  t| t�rLt| d t�rLg }x@| D ]}|�t|�� q4W q�t| t�rbt| �g}q�td� t�  n<t| t�r�t| d t�r�| }nt| t�r�| }ntd� t�  |�	|��
� }|�|�}|�|�}	||	fS )aP  
    Grant Holtes, 15/02/2020
    input:  x, a string or list of strings that have not been preporcessed yet
            modelTuple, a tuple of the loaded models output by loadModel
    output: a list of predictions of the category that the input string(s) belong to

    Requires createAndTrainModel() and loadModel() has been run
    r   z(ERROR: unsupported data type passed as x)r   �
isinstance�listr>   r   r   r   �exitrr   Z	transformry   ZpredictZpredict_proba)
�xZ
modelTupler    r   rs   ZxPreProcessedr'   ZxVectorised�predictionsLabel�predictionsProbabilitiesr-   r-   r.   �getPredictions�  s*    	




r�   )�PdfFileReaderc          	   C   sJ   d}t | d��2}t|dd�}x|jD ]}|�� }||7 }q$W W dQ R X |S )z�
    Grant Holtes, 10/02/2020
    Opens a pdf file, extracts text data

    inputs: str, a path to a PDF file
    outputs: str, a string of all the text in the pdf that could be extracted.

    runtime ~= 0.05sec per pdf
    r   r2   F)�strictN)r   r�   ZpagesZextractText)r   �textDump�f�readerZpageZtextDumpPager-   r-   r.   r   �  s    
r   c                s�  t �|�}t� fdd�|D ��}d}|dkrnx,|D ]$}|d t� d �� � d kr2|}q2W d�|�}t|� n||dkr�td�|�� x,|D ]$}|d t� d �� � d kr�|}q�W d�||�}t|� n"|d	kr�d
}t|� d }|d |fS d|k�rtd� t �d� td� tt j�	||�d�}|d j
}dd� |D �}|�d� t �t j�	|d��}	x<|D ]4}
|
|	k�r^t|
�dk�s^t �t j�	|d|
�� �q^W |||fS )Nc                s0   g | ](}|d t � d �� � d kr(dnd�qS )Nrs   r
   r   )r   )�.0r�   )�namer-   r.   �
<listcomp>  s    z$FindAndLoadModel.<locals>.<listcomp>r   r
   rs   zUsing model {0}z+There are {0} model folders. Remove extras?z${0} model folders found. 
 Using {1}r   z90 model folders found. Train a model before using predict�predictionsz:Making new output folder as 
 'predictions' folder missingzLoad Model files)r�   c             S   s   g | ]}t |��qS r-   )r>   )r�   �cr-   r-   r.   r�   >  s    �NotClassifiedr   )r   r   �sumr   r   r   r   r�   r   r   Zclasses_r   r>   )r�   r"   r&   r)   r#   �iZmodelDirrs   �classesZ
classesDir�class_r-   )r�   r.   �FindAndLoadModel  sD    











r�   z.pdfc          	   C   s�   t �|�}d|kr$td� t �d� t �t j�|d��}g }xH|D ]@}x:| D ]2}||t|� d� krL|�t j�|d|�� P qLW qBW |S )z�
	Grant Holtes 24/5/20
	returns a list of acceptable input file locations 
	full path is used eg "input_files_to_be_sorted/FILENAME.pdf"
	Zinput_files_to_be_sortedzGMaking new output folder as 
 'input_files_to_be_sorted' folder missingN)r   r   r   r   r   r   r   r   )�acceptedFileTypesr"   r&   �filesZfilesToBeSortedZfile_ZfileTyper-   r-   r.   �getTargetFileDirsH  s    




r�   )�WordPunctTokenizer)�PorterStemmerc            �   C   sz  ddddddddd	d
dddddddddddddddddddddd d!d"d#d$d%d&d'd(d)d*d+d,d-d.d/d0d1d2d3d4d5d6d7d8d9d:d;d<d=d>d?d@dAdBdCdDdEdFdGdHdIdJdKdLdMdNdOdPdQdRdSdTdUdVdWdXdYdZd[d\d]d^d_d`dadbdcdddedfdgdhdidjdkdldmdndodpdqdrdsdtdudvdwdxdydzd{d|d}d~dd�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�d�g�a t� at� ad S )�NZwouldnZwhichzit'szdidn'tZherZshezhasn'tzyou'veZsomeZmore�isZcouldnZhersZnoZsoZours�dz	shouldn'tZoffZwasZaboutzmightn'tZownZaboveZmost�outZyouZjustzhadn'tZhaven�o�onceZshouldnZfew�yZveZyourZ	ourselvesZwhyZdoes�meZatZmustnzyou'dZthenZweren�reZbelowZshouldZdoesnZwhenzshe'sZcanZof�thatzweren'tZafter�anyz	should'veZwasn�tZveryZtheseZyourselfZnorZmyZwonZhisZbothZsameZyoursZonlyZbutZour�itZhasZbezwasn'tZherselfZitsZmightnzneedn't�asZamZareZtheyZtheirZdoingZduringZagain�allzdoesn'tZbetweenZunderZoverzthat'llzhaven't�thisZwillZuntilzcouldn'tZhadZmyselfZbecauseZthanzwon'tZheZhave�withZdonZhadnZwhoZupzwouldn'tZainZthemr�   ZthroughZaren�hereZ
themselveszshan't�ifZwhatZmaZ
yourselvesZtheirs�aZagainstZbeing�to�whereZonZhavingZhimselfZeachzyou'llzdon'tZfurtherzisn't�while�inZhowZsuchrh   �fromZneednZthereZhasnZtoo�m�or�notZdidnZwhomZdownZshanZllzyou're�szmustn'tZhimZwereZanZwezaren'tZbyZbeenZtheZitselfZbeforeZdidZinto�and�forZdo�otherZthoseZisn)�	stopWordsr�   �	tokenizerr�   �stemmerr-   r-   r-   r.   r   p  s    � kr   c          	      s�   d� � �fdd�t dt��� �D �}d}x(|D ] }|t�dd|tjtjB �7 }q.W |���� �t���}dd� |D �}|r�g }x|D ]}|�	t
�|�� q�W d�|�S d�|�S d	S )
a#  
    Grant Holtes, 15/02/2020
    input: str, a string
    output: str, a normalised string

    requires setupTextPreProcess() is run before calling

    Time to run ~= 0.0150 secounds per page of text with stemming,
                ~= 0.0010 secounds per page of text with no stemming
    r   c                s   g | ]}�||�  � �qS r-   r-   )r�   r�   )�	maxLengthr*   r-   r.   r�   �  s    z"preprocessText.<locals>.<listcomp>r   r   z[^a-zA-Z\s]c             S   s   g | ]}|t kr|�qS r-   )r�   )r�   �tokenr-   r-   r.   r�   �  s    � N)�ranger   r�   �sub�I�Are   r�   �tokenizer   r�   �stemr   )r*   r�   Z
substringsZregexProcessedTextZ	substringZ
textTokensZnormalizedTokens�charr-   )r�   r*   r.   r   |  s     
 


r   c             C   s   t j| ||ddd�S )z� 
    Grant Holtes 10/5/20
    Structured default format button
    inputs: self, text (str), command in the form self.FUNCTION
    outputs: a tk button
    Zblack�   )r*   �commandZ
backgroundZborderwidth)�tk�Button)�selfr*   r�   r-   r-   r.   �defaultButton�  s    
r�   c               C   s   t �� �d�S )Nz%Y%m%d-%H%M%S)rg   rh   ri   r-   r-   r-   r.   rj   �  s    c              C   s�   t tdd�rhtj�tj�tj��} d| kr�t| �}d}x*tt	|�d �D ]}tj�
||| �}qHW |} ntr�tj�tj�t��} | S )N�frozenFZMacOSr   �   )�getattr�sysr   r   �abspath�dirname�
executable�splitallr�   r   r   �__file__)�applicationPathZappPathListZnewPathr�   r-   r-   r.   �
GetAppPath�  s    r�   c             C   sr   g }xht j�| �}|d | kr2|�d|d � P q|d | krR|�d|d � P q|d } |�d|d � qW |S )Nr   r
   )r   r   �split�insert)r   Zallparts�partsr-   r-   r.   r�   	  s    r�   c                   sP   e Zd Zd� fdd�	Zdd� Zdd� Zd	d
� Zddd�Zdd� Zdd� Z	�  Z
S )�DocumentClassifierAppNr   c                s@   t � �|� || _| ��  | ��  d| _t� | _d| _|| _	d S )N�
SortStream�K   )
�super�__init__�master�pack�createUIr�   r�   r�   �confidenceValue�
privateKey)r�   r�   �globalPrivateKey)�	__class__r-   r.   r�     s    zDocumentClassifierApp.__init__c             C   s�  t j| dd�| _| jjddt jt j ddd� t j| dd�| _| jjddt jdd	� t �� | _| j�	d
� t j| | jd�| _
| j
jddt jdd	� t j| d| jdd�| _| jjddt jdd	� t j| d| jdd�| _| jjddt jdd	� t j| ddt jd�| _| j�	d� | jjddt jdd	� t j| dd�| _| jjddt jdd	� t j| d| jdd�| _| jjddt jdd	� t j| dd| jdd�| _| jjddt jdd	� d S )NzDocument Classification System)r*   r
   �   ru   )r,   �column�sticky�padx�padyzLicence: XYZ Ltd, 2020�   )r,   r�   r�   r�   �-)�textvariabler�   ZInstructions)r*   r�   �widthzPredict Classes�   r   r   r   )Zfrom_r�   Zorientr�   zConfidence (%)r�   zBuild Model from Data�   �Quit�red)r*   �fgr�   r�   )r�   �Label�AppName�grid�W�N�Licence�	StringVar�statusValue�setr#   r�   �OpenInstructionsZINSTRUCTIONS_Button�E�PredictClassesZPREDICT_ButtonZScaleZ
HORIZONTAL�
confidenceZconfidenceLab�BuildModelFromDataZBuildModelFromData_Button�QuitPressed�quit)r�   r-   r-   r.   r�   &  s@    





zDocumentClassifierApp.createUIc             C   s*   t d� t | j� | j�d�| j�� dS )NzOpenInstructions_Button PRESSEDzCurrent application path:{0}T)r   r�   r   r  r   )r�   r-   r-   r.   r  Q  s    
z&DocumentClassifierApp.OpenInstructionsc             C   s�  t d� t� }t d� | j�d� | jd | }td|| jd�\}}tj�	| j|d �}|�rtt d� | j�d	� g }t
|d
��(}t�|�}x|D ]}	|�|	� q�W W d Q R X t�|dd � �}t d� | j�d� | jd | }
t�tj�	| j|
�� t|d d �df |d d �df �dd�|d d�df |d d�df �dd�|
ddd| jd�	 t�|� t d� | j�d� n:| j�|� yt�|� W n tk
�r�   t d� Y nX dS )Nz!BuildModelFromData_Button PRESSEDzBuilding datasetzBuilding dataset...ZbuiltDataset_T)r    r!   r"   z.csvzLoading datasetzLoading dataset...�rr
   zTraining modelzTraining Model...rs   r   rB   �2   i�  �   )r{   r|   r}   r~   r"   ZDonezFailed to remove dataset)r   rj   r   r  r�   r/   r�   r   r   r   r   r   r�   r   �nprm   r   r�   Zreshape�remover9   )r�   Z	timestampr!   ZbuildDatasetSatatusr$   Z
datasetLocZloadedDatasetr+   r�   r,   ZmodelLocationr-   r-   r.   r  W  sL    



z(DocumentClassifierApp.BuildModelFromDatar   �ffffff�?c             C   sr  t d� | j�� | _t| j| j�\}}}| j�|� t	dg| jd�}t
|�dkr\| j�d� dddd	gg}x*|D ]"}|d
krp|d �dt|� � qpW �x�tdt
|�|�D �]�}	g g  }
}xPt|�D ]D}y(||	|  }|�|� |
�t|�� W q� tk
�r   Y q�X q�W t|
|�\}}�x>tt
|��D �],}	||	 ||	 ||	   }}}|�� }t |||� t|�}tj�|�d }| jd }||k�r�|d t�  d | }t�|tj�| jd||�� |||dg}x|D ]}|�|� �q�W |�|� nft d�|dt|d� �� t�|tj�| jdd
|�� |d
|dg}x|D ]}|�|� �q8W |�|� �q*W q�W t|| jd� dS )NzPredictClasses_Button PRESSEDz.pdf)r�   r"   r   z7Please add files to the input_files_to_be_sorted folderr!   Zclassificationr  �errorsr�   zprobability of class: r
   r   rl   r�   z	No errorszNFile not classified as prediction probability of {1}% was below threshold: {0}r�   z-confidence below threshold, no classification)r"   T)r   r  r\   r�   r�   r�   r�   r   r  r�   r   r   r>   r�   rf   �
IndexErrorr�   �tolist�maxr   r   r�   rj   �replacer   r   �roundrn   )r�   ZprocessingBatchSizeZ	thresholdrs   r�   r#   ZtargetFilesZlogArrayr�   r�   ZtextListZfileListZbatch_iZ
targetFiler�   r�   ZpredictionsLabel_iZpredictionsProbabilities_iZfile_iZpredictionsProbabilityZfileNameOnlyZnewFileNameZfileLogZprobr-   r-   r.   r  �  sV    
 





 
 z$DocumentClassifierApp.PredictClassesc               C   s   dS )NTr-   r-   r-   r-   r.   �
PredictAPI�  s    z DocumentClassifierApp.PredictAPIc             C   s   t d� | j��  d S )Nzquit_Button PRESSED)r   r�   �destroy)r�   r-   r-   r.   r  �  s    z!DocumentClassifierApp.QuitPressed)Nr   )r   r  )�__name__�
__module__�__qualname__r�   r�   r  r  r  r  r  �__classcell__r-   r-   )r�   r.   r�     s   +6
Dr�   c                   s6   e Zd Zd� fdd�	Zdd� Zdd� Zd	d
� Z�  ZS )�	LicencingNr   c                s@   t � �|� || _| ��  | ��  d| _t� | _d| _|| _	d S )Nr�   r�   )
r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   )r�   r�   r�   )r�   r-   r.   r�   �  s    zLicencing.__init__c             C   s8  t j| dd�| _| jjddt jt j ddd� t j| dd�| _| jjddt jdd	� t j| d
d�| _| jjddt jdd	� t �� | _	| j	�
d� t j| | j	d�| _| jjddt jdd	� t �| �| _| jjddt jdd	� t j| d| jdd�| _| jjddt jdd	� t j| dd| jdd�| _| jjddt jdd	� d S )Nr�   )r*   r
   r�   ru   )r,   r�   r�   r�   r�   zLicence: XYZ Ltd, 2020r�   )r,   r�   r�   r�   z(Please enter a valid product code below:r�   r�   )r�   r�   r   ZEnter)r*   r�   r�   r�   r�   r�   )r*   r�   r�   r�   �   )r�   r�   r�   r�   r�   r�   r�   �infor�   r   r  r#   ZEntry�prodKeyr�   rJ   Zsubmitr  r  r  )r�   r-   r-   r.   r�   �  s*    



zLicencing.createUIc             C   s   t d� | j��  d S )Nzquit_Button PRESSED)r   r�   r  )r�   r-   r-   r.   r  	  s    zLicencing.QuitPressedc             C   sV   t d� | j�� }t d�|�� t|d�\}}| j�|� |rRtd| j|| j	d� dS )NzcheckProductKey PRESSEDzProduct key entered: {0})rG   zsortstream.licence)r:   r;   rG   r"   T)
r   r  r\   r   rJ   r   r  rO   r�   r�   )r�   ZproductKeyUserrI   rH   r-   r-   r.   rJ     s    

zLicencing.checkProductKey)Nr   )r  r  r  r�   r�   r  rJ   r  r-   r-   )r�   r.   r  �  s   "r  i�  )r"   r:   r;   r�   Z650x210i�  �   )r�   Z550x210)r�   r�   )Tr   r   r   r   )r   r1   r   )r   r   )r   )r1   r   r   r   )rP   )rB   rP   )rB   rP   )rk   r   rk   )rs   rt   r   ru   r   )rs   rw   rx   r   )T)r   )T)K�__doc__r   Znumpyr  �ModuleNotFoundError�systemZtkinterr[   ZsklearnZPyPDF2ZnltkZpkg_resources.py2_warnZpkg_resourcesr   r   r/   r6   r4   Zhashlibr0   rX   Zurllib.parseZurllibr=   r8   rJ   rO   rE   rF   rd   rf   rg   rj   rn   Zsklearn.feature_extraction.textro   Zsklearn.preprocessingrp   Zsklearn.linear_modelrq   rr   r�   r�   r�   r�   r   r�   r�   r�   Z	nltk.stemr�   r�   r   r   r�   r�   r�   r�   r�   ZFramer�   r  r   Z	TkVersionr�   r�   ZvalidLicenceZTk�root�titleZgeometryZminsizeZapprc   Zmainloopr-   r-   r-   r.   �<module>   s�   







R


%

 
$
!
    
)   

4
1
g BE






