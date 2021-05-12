from matplotlib import pyplot as plt

vals = [-12, -2, 4, -3, 4, 8]
attempts = [i for i in range(len(vals))]

plt.bar(attempts, vals)
plt.axhline(y=0, color='k', linestyle='--')
plt.xlabel('Attempt')
plt.ylabel('Error (cm)')
plt.title('Lateral End Position Error of Fiducial Following')
plt.savefig('images/validation.png')