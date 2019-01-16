from import_modules import *

#First step: Surface Normals from Shading
# nz = number of non-zero values in the mask
# J = array of size/shape (3,nz) to calculate normals
# M = (S^−1)J = (S/1)*J to obtain the albedo modulated normal field for each image 
#Second step: Re-integration of surface from Normals with premade fumctions

# beethoven_mat_I.shape = (256,256,3) 
# beethoven_mat_mask.shape = (256,256)
# beethoven_mat_S.shape = (3,3)

#beethoven_mat = read_data_file('Beethoven.mat')
beethoven_mat = loadmat('Beethoven.mat')

#3D array I of size (m,n,k) where (m,n) is the size of each image and k is the number of views
beethoven_mat_I = beethoven_mat['I']
#2D binary array mask of size (m, n). Only pixels with values 1 should be used for Photometric stereo
beethoven_mat_mask = beethoven_mat['mask']
#an array S of light vectors, of size (k, 3), where line i represents the directional light Si that was used to obtain image I(:,:,i).
beethoven_mat_S = beethoven_mat['S']

image1= beethoven_mat_I[:,:,0]
image2= beethoven_mat_I[:,:,1]
image3= beethoven_mat_I[:,:,2]
# plt.imshow(image1, cmap= 'gray')
# plt.show(block=False)
# input('press <ENTER> to continue')

#counts the amount of non-zero values in the mask nz = 28898
nz = np.count_nonzero(beethoven_mat_mask == 1)
#creates the J array
#J = np.zeros(shape=(3,nz))


# List of vectors with pixel values for each image, where the mask is non-zero
J = []
for i in range(0,beethoven_mat_I.shape[2]):
    J.append(beethoven_mat_I[:,:,i][np.where(beethoven_mat_mask)])
J = np.array(J)
print(J.shape)

# obtain the albedo modulated normal field as M = S−1J. 1/S*J
#S=1/beethoven_mat_S 
#M = S.dot(J)

S=np.linalg.inv(beethoven_mat_S)
M=np.dot(S,J)
print(M.shape)

albedo = np.linalg.norm(M, axis = 0) # slide 64
albedo.shape

albedo_image = np.zeros(beethoven_mat_mask.shape)
print(albedo_image.shape)

albedo_image[np.where(beethoven_mat_mask)] = albedo
# plt.imshow(albedo_image, cmap= 'gray')
# plt.show(block=False)
# input('press <ENTER> to continue')

n1 = np.array(M[0]) 
n2 = np.array(M[1]) 
n3 = np.array(M[2]) 

n = (1/albedo)*M #normal M is the field of all the normals

n1 = np.zeros((beethoven_mat_mask.shape))
n1[np.where(beethoven_mat_mask)] = n[0]
n2 = np.zeros((beethoven_mat_mask.shape))
n2[np.where(beethoven_mat_mask)] = n[1]
n3 = np.zeros((beethoven_mat_mask.shape))
n3[np.where(beethoven_mat_mask)] = n[2]
n3.dtype

z = unbiased_integrate(n1, n2, n3, beethoven_mat_mask, order = 2)

display_depth_mayavi(z)