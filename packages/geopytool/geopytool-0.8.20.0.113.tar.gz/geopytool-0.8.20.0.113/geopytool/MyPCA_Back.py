from geopytool.ImportDependence import *
from geopytool.CustomClass import *


class MyPCA(AppForm):
    Lines = []
    Tags = []
    WholeData = []
    settings_backup=pd.DataFrame()
    description = 'PCA'
    unuseful = ['Name',
                'Mineral',
                'Author',
                'DataType',
                'Label',
                'Marker',
                'Color',
                'Size',
                'Alpha',
                'Style',
                'Width',
                'Tag']
    data_to_test =pd.DataFrame()
    switched = False
    text_result = ''
    whole_labels=[]
    pca = PCA(n_components='mle')

    n=6

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self._df = df

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to PCA')



        self.settings_backup = self._df
        ItemsToTest = ['Label','Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']
        for i in self._df.columns.values.tolist():
            if i not in ItemsToTest:
                self.settings_backup = self.settings_backup.drop(i, 1)
        #print(self.settings_backup)


        self.result_to_fit= self.Slim(self._df)


        #print(self.result_to_fit)
        #print(self.result_to_fit.shape)

        #self.pca=PCA(n_components='mle')
        try:
            self.pca.fit(self.result_to_fit.values)
            self.evr = (self.pca.explained_variance_ratio_)
            self.ev = (self.pca.explained_variance_)
            self.n = (self.pca.n_components_)
            self.comp = (self.pca.components_)
        except Exception as e:
            self.ErrorEvent(text=repr(e))

        self.create_main_frame()

    def create_main_frame(self):
        self.resize(800,800)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)
        self.setWindowTitle('Principle Component Analysis')
        self.fig = plt.figure(figsize=(12, 6))
        self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.1, bottom=0.1, right=0.9, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.Key_Func)  # int

        self.shape_cb= QCheckBox('&Shape')
        self.shape_cb.setChecked(False)
        self.shape_cb.stateChanged.connect(self.Key_Func)  # int

        self.hyperplane_cb= QCheckBox('&Hyperplane')
        self.hyperplane_cb.setChecked(False)
        self.hyperplane_cb.stateChanged.connect(self.Key_Func)  # int


        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_picture_button = QPushButton('&Save Picture')
        self.save_picture_button.clicked.connect(self.saveImgFile)

        self.save_result_button = QPushButton('&Save PCA Result')
        self.save_result_button.clicked.connect(self.saveResult)

        self.save_Para_button = QPushButton('&Save PCA Para')
        self.save_Para_button.clicked.connect(self.savePara)

        self.load_data_button = QPushButton('&Load Data to Test')
        self.load_data_button.clicked.connect(self.loadDataToTest)

        self.switch_button = QPushButton('&Switch to 2D')
        self.switch_button.clicked.connect(self.switch)


        self.x_element = QSlider(Qt.Horizontal)
        self.x_element.setRange(0, self.n - 1)
        self.x_element.setValue(0)
        self.x_element.setTracking(True)
        self.x_element.setTickPosition(QSlider.TicksBothSides)
        self.x_element.valueChanged.connect(self.Key_Func)  # int
        self.x_element_label = QLabel('component')

        self.y_element = QSlider(Qt.Horizontal)
        self.y_element.setRange(0, self.n - 1)
        self.y_element.setValue(1)
        self.y_element.setTracking(True)
        self.y_element.setTickPosition(QSlider.TicksBothSides)
        self.y_element.valueChanged.connect(self.Key_Func)  # int
        self.y_element_label = QLabel('component')

        self.z_element = QSlider(Qt.Horizontal)
        self.z_element.setRange(0, self.n - 1)
        self.z_element.setValue(2)
        self.z_element.setTracking(True)
        self.z_element.setTickPosition(QSlider.TicksBothSides)
        self.z_element.valueChanged.connect(self.Key_Func)  # int
        self.z_element_label = QLabel('component')


        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()


        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.hbox.addWidget(self.legend_cb)
        self.hbox.addWidget(self.shape_cb)
        self.hbox.addWidget(self.hyperplane_cb)
        self.hbox.addWidget(self.switch_button)
        self.hbox.addWidget(self.load_data_button)
        self.hbox.addWidget(self.save_picture_button)
        self.hbox.addWidget(self.save_result_button)
        self.hbox.addWidget(self.save_Para_button)
        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        for w in [self.x_element_label, self.x_element]:
            self.hbox2.addWidget(w)
            self.hbox2.setAlignment(w, Qt.AlignVCenter)
        for w in [self.y_element_label, self.y_element]:
            self.hbox3.addWidget(w)
            self.hbox3.setAlignment(w, Qt.AlignVCenter)
        for w in [self.z_element_label,self.z_element]:
            self.hbox4.addWidget(w)
            self.hbox4.setAlignment(w, Qt.AlignVCenter)


        if ( self.switched== False):

            self.switch_button.setText('&Switch to 2D')
            self.axes = Axes3D(self.fig, elev=-150, azim=110)
            self.vbox.addLayout(self.hbox4)
        else:
            self.switch_button.setText('&Switch to 3D')
            self.axes = self.fig.add_subplot(111)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)
        #self.show()

    def switch(self):
        self.switched = not(self.switched)
        self.create_main_frame()
        self.Key_Func()

    def Key_Func(self):

        a = int(self.x_element.value())
        b = int(self.y_element.value())
        c = int(self.z_element.value())

        self.axes.clear()
        self.pca.fit(self.result_to_fit.values)
        self.evr = (self.pca.explained_variance_ratio_)
        self.ev = (self.pca.explained_variance_)
        self.n = (self.pca.n_components_)
        self.comp = (self.pca.components_)

        #self.text_result='N Components :' + str(n)+'N Components :' + str(comp)+ '\nExplained Variance Ratio :' + str(evr)+'\nExplained Variance :' + str(ev)


        title=[]
        for i in range(len(self.comp)):
            title.append('Components No.'+ str(i+1))

        self.nvs = zip(title, self.comp)
        self.compdict = dict((title, self.comp) for title, self.comp in self.nvs)
        self.Para=pd.DataFrame(self.compdict)


        self.pca_result = self.pca.fit_transform(self.result_to_fit)


        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]

        for i in range(len(self._df)):
            target = self._df.at[i, 'Label']
            color = self._df.at[i, 'Color']
            marker = self._df.at[i, 'Marker']
            alpha = self._df.at[i, 'Alpha']

            if target not in all_labels:
                all_labels.append(target)
                all_colors.append(color)
                all_markers.append(marker)
                all_alpha.append(alpha)

        self.whole_labels = all_labels

        if(len(self.data_to_test)>0):

            contained = True
            missing = 'Miss setting infor:'

            for i in ['Label', 'Color', 'Marker', 'Alpha']:
                if i not in self.data_to_test.columns.values.tolist():
                    contained = False
                    missing = missing +'\n' + i

            if contained == True:
                pass

                for i in self.data_to_test.columns.values.tolist():

                    if i not in self._df.columns.values.tolist():
                        self.data_to_test=self.data_to_test.drop(columns=i)

                #print(self.data_to_test)

                test_labels=[]
                test_colors=[]
                test_markers=[]
                test_alpha=[]

                for i in range(len(self.data_to_test)):

                    #print(self.data_to_test.at[i, 'Label'])
                    target = self.data_to_test.at[i, 'Label']
                    color = self.data_to_test.at[i, 'Color']
                    marker = self.data_to_test.at[i, 'Marker']
                    alpha = self.data_to_test.at[i, 'Alpha']

                    if target not in test_labels and target not in all_labels:
                        test_labels.append(target)
                        test_colors.append(color)
                        test_markers.append(marker)
                        test_alpha.append(alpha)


                self.whole_labels = self.whole_labels + test_labels

                self.data_to_test_to_fit= self.Slim(self.data_to_test)

                #print(self.data_to_test_to_fit)
                #print(self.data_to_test_to_fit.shape)


                self.load_settings_backup = self.data_to_test
                Load_ItemsToTest = ['Label', 'Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size',
                               'Alpha',
                               'Style', 'Width']
                for i in self.data_to_test.columns.values.tolist():
                    if i not in Load_ItemsToTest:
                        self.load_settings_backup = self.load_settings_backup .drop(i, 1)

                #print(self.load_settings_backup ,self.pca_data_to_test)


                try:
                    self.pca_data_to_test = self.pca.transform(self.data_to_test_to_fit)

                    self.load_result = pd.concat([self.load_settings_backup,pd.DataFrame(self.pca_data_to_test)], axis=1)
                    for i in range(len(test_labels)):
                        if (self.switched == False):
                            self.axes.scatter(self.pca_data_to_test[self.data_to_test_to_fit.index == test_labels[i], a],
                                              self.pca_data_to_test[self.data_to_test_to_fit.index == test_labels[i], b],
                                              self.pca_data_to_test[self.data_to_test_to_fit.index == test_labels[i], c],
                                              color=test_colors[i],
                                              marker=test_markers[i],
                                              label=test_labels[i],
                                              alpha=test_alpha[i])
                        else:
                            self.axes.scatter(self.pca_data_to_test[self.data_to_test_to_fit.index == test_labels[i], a],
                                              self.pca_data_to_test[self.data_to_test_to_fit.index == test_labels[i], b],
                                              color=test_colors[i],
                                              marker=test_markers[i],
                                              label=test_labels[i],
                                              alpha=test_alpha[i])

                            '''
                            if (self.shape_cb.isChecked()):
                                pass
                                XtoFit = self.pca_data_to_test[self.data_to_test_to_fit.index == test_labels[i], a]
                                YtoFit = self.pca_data_to_test[self.data_to_test_to_fit.index == test_labels[i], b]

                                xmin, xmax = min(XtoFit), max(XtoFit)
                                ymin, ymax = min(YtoFit), max(YtoFit)

                                DensityColorMap = 'Blues'
                                DensityAlpha = 0.1

                                DensityLineColor = test_colors[i]
                                DensityLineAlpha = 0.1
                                # Peform the kernel density estimate
                                xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
                                positions = np.vstack([xx.ravel(), yy.ravel()])
                                values = np.vstack([XtoFit, YtoFit])
                                kernelstatus = True
                                try:
                                    st.gaussian_kde(values)
                                except Exception as e:
                                    self.ErrorEvent(text=repr(e))
                                    kernelstatus = False
                                if kernelstatus == True:
                                    kernel = st.gaussian_kde(values)
                                    f = np.reshape(kernel(positions).T, xx.shape)
                                    # Contourf plot
                                    cfset = self.axes.contourf(xx, yy, f, cmap=DensityColorMap, alpha=DensityAlpha)
                                    # Contour plot
                                    cset = self.axes.contour(xx, yy, f, colors=DensityLineColor, alpha=DensityLineAlpha)
                                    # Label plot
                                    self.axes.clabel(cset, inline=1, fontsize=10)

                            
                            '''

                except Exception as e:
                    self.ErrorEvent(text=repr(e))

            else:
                self.ErrorEvent(text=missing)


        self.axes.set_xlabel("component no."+str(a+1))
        self.x_element_label.setText("component no."+str(a+1))

        self.axes.set_ylabel("component no."+str(b+1))
        self.y_element_label.setText("component no."+str(b+1))

        self.begin_result = pd.concat([self.settings_backup,pd.DataFrame(self.pca_result)], axis=1)

        for i in range(len(all_labels)):
            if (self.switched == False):

                self.axes.scatter(self.pca_result[self.result_to_fit.index == all_labels[i], a],
                                  self.pca_result[self.result_to_fit.index == all_labels[i], b],
                                  self.pca_result[self.result_to_fit.index == all_labels[i], c],
                                  color=all_colors[i],
                                  marker=all_markers[i],
                                  label=all_labels[i],
                                  alpha=all_alpha[i])

                self.axes.set_zlabel("component no." + str(c + 1))
                self.z_element_label.setText("component no." + str(c + 1))

            else:

                self.axes.scatter(self.pca_result[self.result_to_fit.index == all_labels[i], a],
                                  self.pca_result[self.result_to_fit.index == all_labels[i], b],
                                  color=all_colors[i],
                                  marker=all_markers[i],
                                  label=all_labels[i],
                                  alpha=all_alpha[i])
                if (self.shape_cb.isChecked()):
                    pass
                    XtoFit = self.pca_result[self.result_to_fit.index == all_labels[i], a]
                    YtoFit = self.pca_result[self.result_to_fit.index == all_labels[i], b]

                    xmin, xmax = min(XtoFit), max(XtoFit)
                    ymin, ymax = min(YtoFit), max(YtoFit)

                    DensityColorMap = 'Greys'
                    DensityAlpha = 0.1

                    DensityLineColor = all_colors[i]
                    DensityLineAlpha = 0.3
                    # Peform the kernel density estimate
                    xx, yy = np.mgrid[xmin:xmax:200j, ymin:ymax:200j]
                    positions = np.vstack([xx.ravel(), yy.ravel()])
                    values = np.vstack([XtoFit, YtoFit])
                    kernelstatus = True
                    try:
                        st.gaussian_kde(values)
                    except Exception as e:
                        self.ErrorEvent(text=repr(e))
                        kernelstatus = False
                    if kernelstatus == True:
                        kernel = st.gaussian_kde(values)
                        f = np.reshape(kernel(positions).T, xx.shape)
                        # Contourf plot
                        cfset = self.axes.contourf(xx, yy, f, cmap=DensityColorMap, alpha=DensityAlpha)
                        # Contour plot
                        cset = self.axes.contour(xx, yy, f, colors=DensityLineColor, alpha=DensityLineAlpha)
                        # Label plot
                        self.axes.clabel(cset, inline=1, fontsize=10)


        if (self.legend_cb.isChecked()):
            self.axes.legend(loc=2,prop=fontprop)

        if (self.hyperplane_cb.isChecked()):

            pass

            if (self.switched == False):

                clf_linear = svm.SVC(C=1.0, kernel='linear')
                clf_poly = svm.SVC(C=1.0, kernel='poly', degree=3)
                clf_rbf = svm.SVC(C=1.0, kernel='rbf', gamma=0.5)
                clf_rbf2 = svm.SVC(C=1.0, kernel='rbf', gamma=0.1)



                clf = svm.SVC(C=1.0, kernel='linear')


                le = LabelEncoder()
                clfs = [clf_linear, clf_poly, clf_rbf, clf_rbf2]
                types = ['Linear Kernel',
                         'Polynomial Kernel with Degree=3',
                         'Gaussian Kernel with $\gamma=0.5$',
                         'Gaussian Kernel with $\gamma=0.1$']

                svm_x = self.pca_result[:, a]
                svm_y = self.pca_result[:, b]
                svm_z = self.pca_result[:, c]
                xx, yy = np.meshgrid(np.arange( min(svm_x), max(svm_x), np.ptp(svm_x) / 100),
                                         np.arange( min(svm_y), max(svm_y), np.ptp(svm_y) / 100))


                le.fit(self.result_to_fit.index)
                class_label = le.transform(self.result_to_fit.index)
                #print(class_label)

                svm_train = pd.concat([pd.DataFrame(svm_x), pd.DataFrame(svm_y), pd.DataFrame(svm_z)], axis=1)

                svm_train = svm_train.values

                # The equation of the separating plane is given by all x so that np.dot(svc.coef_[0], x) + b = 0.
                zz = lambda x, y: (-clf.intercept_[0] - clf.coef_[0][0] * x - clf.coef_[0][1] * y) / clf.coef_[0][2]

                clf.fit(svm_train, class_label)

                #Z = clf.predict(np.c_[xx.ravel(), yy.ravel(), zz.ravel()])
                #Z = Z.reshape(xx.shape)
                #print(Z)

                #self.axes.contourf(xx, yy, zz, Z, cmap='hot', alpha=0.5)
                self.axes.plot_surface(xx, yy, zz(xx,yy).reshape(xx.shape), color= 'grey', alpha=0.5)

            else:
                #clf_linear = svm.SVC(C=1.0, kernel='linear')
                #clf_poly = svm.SVC(C=1.0, kernel='poly', degree=3)
                #clf_rbf = svm.SVC(C=1.0, kernel='rbf', gamma=0.5)
                #clf_rbf2 = svm.SVC(C=1.0, kernel='rbf', gamma=0.1)

                clf = svm.SVC(C=1.0, kernel='linear')
                svm_x = self.pca_result[:, a]
                svm_y = self.pca_result[:, b]

                xx, yy = np.meshgrid(np.arange( min(svm_x), max(svm_x), np.ptp(svm_x) / 100),
                                         np.arange( min(svm_y), max(svm_y), np.ptp(svm_y) / 100))

                le = LabelEncoder()
                le.fit(self.result_to_fit.index)
                class_label=le.transform(self.result_to_fit.index)
                svm_train= pd.concat([pd.DataFrame(svm_x),pd.DataFrame(svm_y)], axis=1)

                svm_train=svm_train.values
                clf.fit(svm_train,class_label)
                Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
                Z = Z.reshape(xx.shape)
                self.axes.contourf(xx, yy, Z, cmap='hot', alpha=0.2)


        self.result = pd.concat([self.begin_result , self.load_result], axis=0).set_index('Label')
        self.canvas.draw()



    def Distance_Calculation(self):

        #print(self.whole_labels)
        distance_result={}

        for i in range(len(self.whole_labels)):
            distance_result[self.whole_labels[i]] = []

        #print(distance_result)


        self.pca_result[self.result_to_fit.index == self.whole_labels[0], 0]

        #print(self.pca_result)

        try:
            #print(self.pca_data_to_test)
            self.pca_data_to_test[self.data_to_test_to_fit.index == self.whole_labels[0], 0]
        except Exception as e:
            pass
            #self.ErrorEvent(text=repr(e))


