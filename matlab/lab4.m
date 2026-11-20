clc; clear; close all;
rng(1)

EbN0dB = 0:10;

N = 2000;
targetErr = 100;
maxBits = 5e5;

BER = zeros(size(EbN0dB));

for k = 1:length(EbN0dB)

    err = 0;
    total = 0;

    nv = 1/(4*10^(EbN0dB(k)/10));

    while err < targetErr && total < maxBits

        % Random bits
        b = randi([0 1],1,N);

        % Differential encoding
        d = zeros(size(b));
        for i = 2:N
            d(i) = xor(d(i-1),b(i));
        end

        % Even length
        if mod(N,2)
            d(end+1)=0;
        end

        % OQPSK mapping
        I = 2*d(1:2:end)-1;
        Q = 2*d(2:2:end)-1;

        tx = (I + 1i*Q)/sqrt(2);

        % AWGN
        noise = sqrt(nv) * ...
            (randn(size(tx)) + 1i*randn(size(tx)));

        rx = tx + noise;

        % Demod
        rI = real(rx)>=0;
        rQ = imag(rx)>=0;

        r = zeros(1,length(d));
        r(1:2:end)=rI;
        r(2:2:end)=rQ;

        r = r(1:N);

        % Differential decoding
        dec = zeros(size(r));

        for i = 2:N
            dec(i)=xor(r(i-1),r(i));
        end

        err = err + sum(b ~= dec);

        total = total + N;
    end

    BER(k)=max(err/total,0.5/total);

    fprintf('Eb/N0=%2d | BER=%.3e\n', ...
        EbN0dB(k), BER(k));
end

figure;
semilogy(EbN0dB,BER,'o-','LineWidth',2)

grid on
xlabel('Eb/N0 (dB)')
ylabel('BER')

title('Differentially Encoded OQPSK in AWGN')

legend('Diff. OQPSK')