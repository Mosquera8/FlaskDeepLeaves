



class DepthwiseSeparableConv(nn.Module):
    def __init__(self, in_channels, out_channels, stride):
        super(DepthwiseSeparableConv, self).__init__()
        self.depthwise = nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=stride, padding=1, groups=in_channels)
        self.pointwise = nn.Conv2d(in_channels, out_channels, kernel_size=1)

    def forward(self, x):
        x = self.depthwise(x)
        x = self.pointwise(x)
        return x

class MobileNetV1(nn.Module):
    def __init__(self, num_classes=5, dropout_prob=0.5):
        super(MobileNetV1, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            DepthwiseSeparableConv(32, 64, 1),
            nn.ReLU(inplace=True),
            DepthwiseSeparableConv(64, 128, 2),
            nn.ReLU(inplace=True),
            DepthwiseSeparableConv(128, 128, 1),
            nn.ReLU(inplace=True),
            DepthwiseSeparableConv(128, 256, 2),
            nn.ReLU(inplace=True),
            DepthwiseSeparableConv(256, 256, 1),
            nn.ReLU(inplace=True),
            DepthwiseSeparableConv(256, 512, 2),
            nn.ReLU(inplace=True),
            DepthwiseSeparableConv(512, 512, 1),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d(1)
        )
        self.fc = nn.Linear(512, num_classes)
        self.dropout = nn.Dropout(dropout_prob) # Regularización

    def forward(self, x):
        x = self.model(x)
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        x = self.fc(x)
        return x